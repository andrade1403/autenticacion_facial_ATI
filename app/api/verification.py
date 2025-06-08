import cv2
import tempfile
import numpy as np
from app.models.login import LogIn
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, File
from app.utils.containers import DBConnection
from app.services.userDB import UserCRUDService
from app.utils.verify_token import verify_token
from app.services.logInDB import LogInCRUDService
from app.services.embedding import extractEmbedding, compareEmbeddings
from app.services.faceRegistrationDB import FaceRegistrationCRUDService

#Crear un router para manejar las rutas de usuarios
router = APIRouter()

#Creamos instancia de variables de entorno
container_users = DBConnection().getContainer('users')
container_faces = DBConnection().getContainer('faces_registration')
container_login = DBConnection().getContainer('logins')

#Creamos una instancia del servicio de CRUD de rostros registrados
user_service = UserCRUDService(container_users)
faces_service = FaceRegistrationCRUDService(container_faces)
logins_service = LogInCRUDService(container_login)

@router.post('/image')
def verificationUser(token = Depends(verify_token), image: bytes = File(...), threshold: float = 0.85):
    #Traemos el usuario de la base de datos usando el ID del token
    success, data = user_service.getUserByIdDB(token['Id'])

    if not success:
        return JSONResponse(status_code = 404, content = {'message': 'El Usuario no existe en la base de datos', 'error': data})
    
    #Validamos que las imagenes no sean nulas
    if not image:
        return JSONResponse(status_code = 422, content = {'message': 'Debe enviar las imagen del rostro', 'error': 'Imagen nulas'})

    #Convertimos la imagen a un arreglo de numpy
    imagen_np = np.frombuffer(image, np.uint8)

    #Decodificamos la imagen
    image_decode = cv2.imdecode(imagen_np, cv2.IMREAD_COLOR)

    #Extraemos el vector de embedding de la imagen
    success, embedding = extractEmbedding(image_decode)

    #Traemos el registro de cara del usuario
    success, face_registration = faces_service.getFaceRegisterByUserIdDB(token['Id'])

    #Validamos si los embeddings iguales
    for face in face_registration:
        #Comparamos las distancias
        distancia = compareEmbeddings(embedding, face['embeddingVector'])
        print(distancia)
        #Validamos si la distancia es menor al umbral
        if distancia < threshold:
            #Creamos un nuevo registro de inicio de sesion
            log_in = LogIn(userId = token['Id'], resultado = False, distancia = distancia)
            success, data = logins_service.createLogInDB(log_in)

            #Validamos si hubo un error al crear el registro de inicio de sesion
            if not success:
                return JSONResponse(status_code = 400, content = {'message': 'Error al crear el registro de inicio de sesión', 'error': data})

            return JSONResponse(status_code = 401, content = {'message': 'Usuario no verificado', 'error': 'No se pudo verificar al usuario con la imagen proporcionada'})
    
    #Creamos un nuevo registro de inicio de sesion
    log_in = LogIn(userId = token['Id'], distancia = distancia)
    success, data = logins_service.createLogInDB(log_in)

    #Validamos si hubo un error al crear el registro de inicio de sesion
    if not success:
        return JSONResponse(status_code = 400, content = {'message': 'Error al crear el registro de inicio de sesión', 'error': data})

    return JSONResponse(status_code = 200, content = {'message': 'Usuario verificado correctamente', 'user': data})

@router.get('/logins')
def getLogins():
    #Traemos usuarios con rostros registrados de la base de datos
    success, data = logins_service.listLogIns()
   
    #Validamos si hubo un error al traer los usuarios
    if not success:
        return JSONResponse(status_code = 400, content = {'message': 'Error al traer todos los logins', 'error': data})
    
    return JSONResponse(status_code = 200, content = {'message': 'Logins traídos correctamente', 'logins': data})
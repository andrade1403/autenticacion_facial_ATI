import cv2
import tempfile
import numpy as np
from datetime import datetime
from app.models.users import User
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, File
from app.utils.containers import DBConnection
from app.services.userDB import UserCRUDService
from app.utils.verify_token import verify_token
from app.services.embedding import extractEmbedding
from app.models.registration import FaceRegistration
from app.services.faceRegistrationDB import FaceRegistrationCRUDService

#Crear un router para manejar las rutas de usuarios
router = APIRouter()

#Creamos instancia de variables de entorno
container_users = DBConnection().getContainer('users')
container_faces = DBConnection().getContainer('faces_registration')

#Creamos una instancia del servicio de CRUD de rostros registrados
user_service = UserCRUDService(container_users)
faces_service = FaceRegistrationCRUDService(container_faces)

@router.post('/image')
def registerImageFace(token = Depends(verify_token), image: bytes = File(...)):
    #Traemos el usuario de la base de datos usando el ID del token
    success, data = user_service.getUserByIdDB(token['Id'])

    if not success:
        #Creamos el usuario si no existe en la base de datos
        user = User(id = token['Id'], name = token['FullName'], email = token[list(token.keys())[0]])
        success_create, data_create = user_service.createUserDB(user)

        #Validamos si hubo un error al crear el usuario
        if not success_create:
            return JSONResponse(status_code = 400, content = {'message': 'Error al crear el usuario', 'error': data_create})
    
    #Validamos que las imagenes no sean nulas
    if not image:
        return JSONResponse(status_code = 422, content = {'message': 'Debe enviar las tres imagenes del rostro', 'error': 'Imagenes nulas'})

    #Convertimos la imagen a un arreglo de numpy
    imagen_np = np.frombuffer(image, np.uint8)

    #Decodificamos la imagen
    image_decode = cv2.imdecode(imagen_np, cv2.IMREAD_COLOR)

    #Extraemos el vector de embedding de la imagen
    success, embedding = extractEmbedding(image_decode)
    
    #Validamos si hubo un error al extraer el embedding
    if not success:
        return JSONResponse(status_code = 422, content = {'message': f'Error al procesar la imagen', 'error': embedding})
        
    #Creamos objeto con el registro de cara
    face_registration = FaceRegistration(userId = token['Id'], embeddingVector = embedding)

    #Creamos el registro de cara en la base de datos
    success, data_img = faces_service.createFaceRegistrationDB(face_registration)
    print(data_img)
    #Validamos si hubo un error al crear el registro de cara
    if not success:
        return JSONResponse(status_code = 400, content = {'message': 'Error al registrar el rostro', 'error': data_img})
    
    return JSONResponse(status_code = 200, content = {'message': 'Rostro registrado correctamente', 'data': data_img})

@router.post('/video')
async def registerVideoFace(token = Depends(verify_token), video = File(...)):
    #Traemos el usuario de la base de datos usando el ID del token
    success, data = user_service.getUserByIdDB(token['Id'])

    if not success:
        #Creamos el usuario si no existe en la base de datos
        user = User(id = token['Id'], name = token['FullName'], email = token[list(token.keys())[0]])
        success_create, data_create = user_service.createUserDB(user)

        #Validamos si hubo un error al crear el usuario
        if not success_create:
            return JSONResponse(status_code = 400, content = {'message': 'Error al crear el usuario', 'error': data_create})
    
    #Validamos que las imagenes no sean nulas
    if not video:
        return JSONResponse(status_code = 422, content = {'message': 'Debe enviar un video', 'error': 'Video nulo'})

    #Leemos el video del cuerpo de la peticion
    with tempfile.NamedTemporaryFile(delete=False, suffix = '.mp4') as tmp:
        tmp.write(await video.read())
        tmp_path = tmp.name

    #Capturar el primer frame
    cap = cv2.VideoCapture(tmp_path)
    success_frame, frame = cap.read()
    cap.release()

    #Validamos si hubo un error al extraer el frame del video
    if not success_frame:
        return JSONResponse(status_code = 422, content = {'message': 'No se pudo leer un frame válido del video'})

    #Extraemos el vector de embedding del video
    success, embedding = extractEmbedding(frame)

    #Validamos si hubo un error al extraer el embedding
    if not success:
        return JSONResponse(status_code = 422, content = {'message': f'Error al procesar el video {video.filename}', 'error': embedding})
        
    #Creamos objeto con el registro de cara
    face_registration = FaceRegistration(userId = token['Id'], embeddingVector = embedding)

    #Modificamos la fecha de registro
    face_registration.fechaRegistro = datetime.strftime(face_registration.fechaRegistro, '%Y-%m-%d')

    #Creamos el registro de cara en la base de datos
    success, data_video = faces_service.createFaceRegistrationDB(face_registration)

    #Validamos si hubo un error al crear el registro de cara
    if not success:
        return JSONResponse(status_code = 400, content = {'message': f'Error al registrar el rostro {video}', 'error': data_video})
    
    return JSONResponse(status_code = 200, content = {'message': 'Rostro registrado correctamente', 'data': data_video})

@router.get('/faces')
def getRegisterFaces():
    #Traemos usuarios con rostros registrados de la base de datos
    success, data = faces_service.listFacesRegister()
   
    #Validamos si hubo un error al traer los usuarios
    if not success:
        return JSONResponse(status_code = 400, content = {'message': 'Error al traer todos los usuarios con rostros registrados', 'error': data})
    
    return JSONResponse(status_code = 200, content = {'message': 'Usuarios registrados con rostro traidos correctamente', 'faces': data})

@router.delete('/faces/delete')
def deleteFaceRegister():
    #Borramos el contenedor de rostros registrados
    success, data = DBConnection().deleteContainer('faces_registration')
    success, data = DBConnection().deleteContainer('users')

    #Validamos si hubo un error al borrar el contenedor
    if not success:
        return JSONResponse(status_code = 400, content = {'message': 'Error al borrar el contenedor de rostros registrados', 'error': data})
    
    return JSONResponse(status_code = 200, content = {'message': 'Contenedor de rostros registrados borrado correctamente', 'data': data})

@router.get('/faces/user/{user_id}')
def getFaceRegisterByUserId(user_id: str, token = Depends(verify_token)):
    #Traemos los registros de cara por ID de usuario
    success, data = faces_service.getFaceRegisterByUserIdDB(user_id)

    #Validamos si hubo un error al traer los registros de cara
    if not success:
        return JSONResponse(status_code = 400, content = {'message': f'Error al traer los registros de cara del usuario {user_id}', 'error': data})
    
    return JSONResponse(status_code = 200, content = {'message': f'Registros de cara del usuario {user_id} traidos correctamente', 'faces': data})


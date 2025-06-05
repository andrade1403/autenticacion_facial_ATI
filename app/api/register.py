import cv2
import numpy as np
from fastapi import APIRouter, Depends, File
from fastapi.responses import JSONResponse
from app.utils.verify_token import verify_token
from app.models.registration import FaceRegistration
from app.services.userDB import createUser, getUserById
from app.services.faceRegistrationDB import createFaceRegistration

#Crear un router para manejar las rutas de usuarios
router = APIRouter()

@router.post('/register')
async def registerFace(token = Depends(verify_token), image = File(...)):
    #Traemos el usuario de la base de datos usando el ID del token
    success, data = getUserById(token['Id'])

    if not success:
        #Creamos el usuario si no existe en la base de datos
        success_create, data_create = createUser(id = token['Id'], name = token['FullName'], email = token['name'])

        #Validamos si hubo un error al crear el usuario
        if not success_create:
            return JSONResponse(status_code = 400, content = {'message': 'Error al crear el usuario', 'error': data_create})
    

    #Leemos la imagen del cuerpo de la peticion
    contenido_imagen = await image.read()

    #Convertimos la imagen a un arreglo de numpy
    imagen_np = np.frombuffer(contenido_imagen, np.uint8)

    #Decodificamos la imagen
    image_decode = cv2.imdecode(imagen_np, cv2.IMREAD_COLOR)

    #Extraemos el vector de embedding de la imagen
    try:
        embedding = face_engine.get_embedding(image_decode)

    except Exception as e:
        return JSONResponse(status_code = 422, content={'message': 'No se pudo procesar el rostro', 'error': str(e)})
    
    #Creamos objeto con el registro de cara
    face_registration = FaceRegistration(userId = token['Id'], embeddingVector = embedding)

    #Creamos el registro de cara en la base de datos
    success, data = createFaceRegistration(face_registration)

    #Validamos si hubo un error al crear el registro de cara
    if not success:
        return JSONResponse(status_code = 400, content = {'message': 'Error al registrar el rostro', 'error': data})
    
    return JSONResponse(status_code = 200, content = {'message': 'Rostro registrado correctamente', 'data': data})
    

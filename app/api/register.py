import cv2
import tempfile
import numpy as np
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, File
from app.utils.verify_token import verify_token
from app.services.embedding import extractEmbedding
from app.models.registration import FaceRegistration
from app.services.userDB import createUserDB, getUserByIdDB
from app.services.faceRegistrationDB import createFaceRegistration

#Crear un router para manejar las rutas de usuarios
router = APIRouter()

@router.post('/image')
async def registerImageFace(token = Depends(verify_token), image = File(...)):
    #Traemos el usuario de la base de datos usando el ID del token
    success, data = getUserByIdDB(token['Id'])

    if not success:
        #Creamos el usuario si no existe en la base de datos
        success_create, data_create = createUserDB(id = token['Id'], name = token['FullName'], email = token['name'])

        #Validamos si hubo un error al crear el usuario
        if not success_create:
            return JSONResponse(status_code = 400, content = {'message': 'Error al crear el usuario', 'error': data_create})
    
    #Validamos que las imagenes no sean nulas
    if not image:
        return JSONResponse(status_code = 422, content = {'message': 'Debe enviar las tres imagenes del rostro', 'error': 'Imagenes nulas'})

    #Leemos la imagen del cuerpo de la peticion
    contenido_imagen = await image.read()

    #Convertimos la imagen a un arreglo de numpy
    imagen_np = np.frombuffer(contenido_imagen, np.uint8)

    #Decodificamos la imagen
    image_decode = cv2.imdecode(imagen_np, cv2.IMREAD_COLOR)

    #Extraemos el vector de embedding de la imagen
    success, embedding = extractEmbedding(image_decode)

    #Validamos si hubo un error al extraer el embedding
    if not success:
        return JSONResponse(status_code = 422, content = {'message': f'Error al procesar la imagen {image.filename}', 'error': embedding})
        
    #Creamos objeto con el registro de cara
    face_registration = FaceRegistration(userId = token['Id'], embeddingVector = embedding)

    #Creamos el registro de cara en la base de datos
    success, data_img = createFaceRegistration(face_registration)

    #Validamos si hubo un error al crear el registro de cara
    if not success:
        return JSONResponse(status_code = 400, content = {'message': f'Error al registrar el rostro {image}', 'error': data_img})
    
    return JSONResponse(status_code = 200, content = {'message': 'Rostro registrado correctamente', 'data': data_img})

@router.post('/video')
async def registerVideoFace(token = Depends(verify_token), video = File(...)):
    #Traemos el usuario de la base de datos usando el ID del token
    success, data = getUserByIdDB(token['Id'])

    if not success:
        #Creamos el usuario si no existe en la base de datos
        success_create, data_create = createUserDB(id = token['Id'], name = token['FullName'], email = token['name'])

        #Validamos si hubo un error al crear el usuario
        if not success_create:
            return JSONResponse(status_code = 400, content = {'message': 'Error al crear el usuario', 'error': data_create})
    
    #Validamos que las imagenes no sean nulas
    if not video:
        return JSONResponse(status_code = 422, content = {'message': 'Debe enviar un video', 'error': 'Video nulo'})

    #Leemos el video del cuerpo de la peticion
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
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

    #Creamos el registro de cara en la base de datos
    success, data_video = createFaceRegistration(face_registration)

    #Validamos si hubo un error al crear el registro de cara
    if not success:
        return JSONResponse(status_code = 400, content = {'message': f'Error al registrar el rostro {video}', 'error': data_video})
    
    return JSONResponse(status_code = 200, content = {'message': 'Rostro registrado correctamente', 'data': data_video})
    

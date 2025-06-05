from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.utils.verify_token import verify_token
from app.services.userDB import createUser, getUserById
from app.services.faceRegistrationDB import createFaceRegistration

#Crear un router para manejar las rutas de usuarios
router = APIRouter()

@router.post('/register')
def registerFace(token = Depends(verify_token)):
    #Traemos el usuario de la base de datos usando el ID del token
    success, data = getUserById(token['Id'])

    if not success:
        #Creamos el usuario si no existe en la base de datos
        success_create, data_create = createUser(id = token['Id'], name = token['FullName'], email = token['name'])

        #Validamos si hubo un error al crear el usuario
        if not success_create:
            return JSONResponse(status_code = 400, content = {'message': 'Error al crear el usuario', 'error': data_create})
    

    

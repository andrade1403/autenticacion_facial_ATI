from fastapi import APIRouter
from app.models.users import User
from fastapi.responses import JSONResponse
from app.utils.containers import DBConnection
from app.services.userDB import UserCRUDService

#Crear un router para manejar las rutas de usuarios
router = APIRouter()

#Creamos instancia de variables de entorno
container = DBConnection().getContainer('users')

#Creamos una instancia del servicio de CRUD de usuarios
user_service = UserCRUDService(container)

@router.get('/')
def getUsers():
    #Traemos usuarios de la base de datos
    success, data = user_service.listUsers()

    #Validamos si hubo un error al traer los usuarios
    if not success:
        return JSONResponse(status_code = 400, content = {'message': 'Error al traer todos los usuarios', 'error': data})
    
    return JSONResponse(status_code = 200, content = {'message': 'Usuarios traidos correctamente', 'users': data})

@router.post('/')
def createUser(user: User):
    #Creamos un usuario en la base de datos
    success, data = user_service.createUserDB(user)

    #Validamos si hubo un error al crear el usuario
    if not success:
        return JSONResponse(status_code = 400, content = {'message': 'Error al crear usuario.', 'error': data})
    
    return JSONResponse(status_code = 200, content = {'message': 'Usuario creado exitosamente', 'users': data})
    
@router.get('/{user_id}')
def getUserById(user_id: str):
    #Traemos un usuario por ID
    success, data = user_service.getUserByIdDB(user_id)

    #Validamos si hubo un error al traer el usuario
    if not success:
        return JSONResponse(status_code = 404, content = {'message': 'Error al traer el usuario', 'error': data})
    
    return JSONResponse(status_code = 200, content = {'message': 'Usuario traido correctamente', 'user': data})

@router.delete('{user_id}')
def deleteUserById(user_id: str):
    #Traemos un usuario por ID
    success, data = user_service.deleteUserByIdDB(user_id)

    #Validamos si hubo un error al eliminar el usuario
    if not success:
        return JSONResponse(status_code = 404, content = {'message': 'Error al eliminar el usuario', 'error': data})
    
    return JSONResponse(status_code = 200, content = {'message': 'Usuario eliminado correctamente', 'user': data})
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services.userDB import getUserById, deleteUserById, listUsers

#Crear un router para manejar las rutas de usuarios
router = APIRouter()

@router.get('/users')
def getUsers():
    #Traemos usuarios de la base de datos
    success, data = listUsers()

    #Validamos si hubo un error al traer los usuarios
    if not success:
        return JSONResponse(status_code = 400, content = {'message': 'Error al traer todos los usuarios', 'error': data})
    
    return JSONResponse(status_code = 200, content = {'message': 'Usuarios traidos correctamente', 'users': data})
    
@router.get('/users/{user_id}')
def getUserById(user_id: str):
    #Traemos un usuario por ID
    success, data = getUserById(user_id)

    #Validamos si hubo un error al traer el usuario
    if not success:
        return JSONResponse(status_code = 404, content = {'message': 'Error al traer el usuario', 'error': data})
    
    return JSONResponse(status_code = 200, content = {'message': 'Usuario traido correctamente', 'user': data})

@router.delete('/users/{user_id}')
def deleteUserById(user_id: str):
    #Traemos un usuario por ID
    success, data = deleteUserById(user_id)

    #Validamos si hubo un error al eliminar el usuario
    if not success:
        return JSONResponse(status_code = 404, content = {'message': 'Error al eliminar el usuario', 'error': data})
    
    return JSONResponse(status_code = 200, content = {'message': 'Usuario eliminado correctamente', 'user': data})
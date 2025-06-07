from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.utils.containers import DBConnection

#Crear un router para manejar las rutas de usuarios
router = APIRouter()

@router.delete('/')
def deleteFaceRegister():
    #Borramos el contenedor de rostros registrados
    success, data = DBConnection().deleteContainer('faces_registration')
    success, data = DBConnection().deleteContainer('users')
    success, data = DBConnection().deleteContainer('logins')

    #Validamos si hubo un error al borrar el contenedor
    if not success:
        return JSONResponse(status_code = 400, content = {'message': 'Error al borrar el contenedor de rostros registrados', 'error': data})
    
    return JSONResponse(status_code = 200, content = {'message': 'Contenedor de rostros registrados borrado correctamente', 'data': data})
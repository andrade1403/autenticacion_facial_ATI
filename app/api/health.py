from fastapi import APIRouter
from fastapi.responses import JSONResponse

#Crear un router para manejar las rutas de usuarios
router = APIRouter()

@router.get('/')
def healthCheck():
    #Retornamos un mensaje de salud
    return JSONResponse(status_code = 200, content = {'message': 'API de usuarios funcionando correctamente'})
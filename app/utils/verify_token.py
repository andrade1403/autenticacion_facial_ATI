import os
from dotenv import load_dotenv
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

#Cargar las variables de entorno desde el archivo .env
load_dotenv()

#Firma secreta para verificar token (debería venir de .env)
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'

#Usamos HTTPBearer para extraer el token del header Authorization
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    #Se declara que el token es un string
    print('Verificando token...')
    token = credentials.credentials

    try:
        #Decodificamos y validamos la firma
        token_decode = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM], audience = 'app')
        return token_decode
    
    except JWTError as e:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = f'Token inválido: {str(e)}',
            headers = {'WWW-Authenticate': 'Bearer'})
from fastapi import FastAPI
from app.api import register, auth, users

#Creamos app
app = FastAPI()

#Endpoints
app.include_router(register.router, prefix = '/register')
app.include_router(auth.router, prefix = '/auth')
app.include_router(users.router, prefix = '/users')
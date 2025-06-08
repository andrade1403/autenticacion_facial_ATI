from fastapi import FastAPI
from app.api import register, users, health, delete, verification

#Creamos app
app = FastAPI()

#Registro de endpoints
app.include_router(register.router, prefix = '/register')
app.include_router(verification.router, prefix = '/verification')
app.include_router(users.router, prefix = '/users')
app.include_router(health.router, prefix = '/health')
app.include_router(delete.router, prefix = '/delete')
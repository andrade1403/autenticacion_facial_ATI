import os
from dotenv import load_dotenv

#Cargar variables de entorno desde el archivo .env
load_dotenv()

class Settings:
    #Variables de entorno necesarias para la conexión a Cosmos DB
    COSMOS_URL = os.getenv('COSMOS_URL')
    COSMOS_KEY = os.getenv('COSMOS_KEY')
    DATABASE_NAME = os.getenv('DATABASE_NAME')

    @classmethod
    def validate(cls):
        if not cls.COSMOS_URL or not cls.COSMOS_KEY or not cls.DATABASE_NAME:
            raise ValueError('Faltan variables de entorno requeridas.')

import os
import uuid
from dotenv import load_dotenv
from app.models.users import User
from azure.cosmos import PartitionKey
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosResourceNotFoundError

#Cargar las variables de entorno desde el archivo .env
load_dotenv()

#Variables de entorno
COSMOS_URL = os.getenv('COSMOS_URL')
COSMOS_KEY = os.getenv('COSMOS_KEY')
DATABASE_NAME = os.getenv('DATABASE_NAME')
USERS_CONTAINER_NAME = os.getenv('USERS_CONTAINER_NAME', 'users')

#Validamos que las variables de entorno necesarias esten definidas
if not COSMOS_URL or not COSMOS_KEY or not DATABASE_NAME or not USERS_CONTAINER_NAME:
    raise ValueError('Las variables de entorno COSMOS_URL, COSMOS_KEY, DATABASE_NAME y USERS_CONTAINER_NAME son necesarias.')

#Crear cliente de cosmos
client = CosmosClient(COSMOS_URL, credential = COSMOS_KEY)
db = client.get_database_client(DATABASE_NAME)

try:
    container = db.get_container_client(USERS_CONTAINER_NAME)
    # Forzamos una llamada para verificar si realmente existe
    container.read()

except CosmosResourceNotFoundError:
    container = db.create_container_if_not_exists(
        id=USERS_CONTAINER_NAME,
        partition_key=PartitionKey(path="/id")
    )

#Crear un usuario en la base de datos
def createUserDB(user: User):
    try:
        #Recibimos el usuario y lo volvemos diccionario
        user_dict = user.model_dump()

        #Creamos el usuario en la base de datos
        return True, container.create_item(user_dict)
    
    except Exception as e:
        return False, str(e)

#Leer un usuario por ID
def getUserByIdDB(user_id: str):
    try:
        #Buscamos el usuario por ID
        user = container.read_item(user_id, partition_key = user_id)
        return True, User(**user).model_dump()

    except Exception as e:
        return False, str(e)

#Borrar un usuario por ID
def deleteUserByIdDB(user_id: str):
    try:
        #Borramos el usuario por ID
        return True, container.delete_item(user_id, partition_key = user_id)
    
    except Exception as e:
        return False, str(e)

#Devolver una lista de usuarios
def listUsers():
    try:
        #Leemos todos los usuarios del contenedor
        users = container.read_all_items()
        return True, [User(**user).model_dump() for user in users]

    except Exception as e:
        return False, str(e)
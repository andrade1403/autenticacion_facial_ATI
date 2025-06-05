import os
from dotenv import load_dotenv
from app.models.users import User
from azure.cosmos import CosmosClient

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
container = db.get_container_client(USERS_CONTAINER_NAME)

#Crear un usuario en la base de datos
def createUser(user: User):
    try:
        #Creamos el usuario en la base de datos
        return (True, container.create_item(user.model_dump(by_alias = True)))
    
    except Exception as e:
        return (False, str(e))

#Leer un usuario por ID
def getUserById(user_id: str):
    try:
        #Buscamos el usuario por ID
        user = container.read_item(user_id, partition_key = user_id)
        return (True, User(**user).model_dump(by_alias = True))

    except Exception as e:
        return (False, str(e))

#Borrar un usuario por ID
def deleteUserById(user_id: str):
    try:
        #Borramos el usuario por ID
        return (True, container.delete_item(user_id, partition_key = user_id))
    
    except Exception as e:
        return (False, str(e))

#Devolver una lista de usuarios
def listUsers():
    try:
        #Leemos todos los usuarios del contenedor
        users = container.read_all_items()
        return (True, [User(**user).model_dump(by_alias = True) for user in users])

    except Exception as e:
        return (False, str(e))
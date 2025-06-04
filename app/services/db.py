import os
from app.models.users import User
from azure.cosmos import CosmosClient

#Variables de entorno
COSMOS_URL = os.getenv('COSMOS_DB_URL')
COSMOS_KEY = os.getenv('COSMOS_DB_KEY')
DATABASE_NAME = os.getenv('COSMOS_DB_NAME')
CONTAINER_NAME = os.getenv('COSMOS_DB_CONTAINER', 'Usuarios')

#Validamos que las variables de entorno necesarias esten definidas
if not COSMOS_URL or not COSMOS_KEY or not DATABASE_NAME:
    raise ValueError('Las variables de entorno COSMOS_DB_URL, COSMOS_DB_KEY y COSMOS_DB_NAME son necesarias.')

#Crear cliente de cosmos
client = CosmosClient(COSMOS_URL, credential = COSMOS_KEY)
db = client.get_database_client(DATABASE_NAME)
container = db.get_container_client(CONTAINER_NAME)

#Crear un usuario en la base de datos
def createUser(user: User):
    try:
        #Creamos el usuario en la base de datos
        return (True, container.create_item(user.model_dump()))
    
    except Exception as e:
        return (False, str(e))

#Leer un usuario por ID
def getUserById(user_id: str):
    try:
        #Buscamos el usuario por ID
        user = container.read_item(user_id, partition_key = user_id)
        return (True, User(**user).model_dump())

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
        return (True, [User(**user).model_dump() for user in users])

    except Exception as e:
        return (False, str(e))
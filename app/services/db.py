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
    #Creamos el usuario en la base de datos
    return container.create_item(user.model_dump())

#Leer un usuario por ID
def getUserById(user_id: str):
    try:
        #Buscamos el usuario por ID
        user = container.read_item(user_id, partition_key = user_id)
        return User(**user)
    
    except Exception:
        return {'error': 'Usuario no encontrado en la base de datos.'}

#Borrar un usuario por ID
def deleteUserById(user_id: str):
    try:
        #Borramos el usuario por ID
        container.delete_item(user_id, partition_key = user_id)
    
    except Exception:
        return {'error': 'Usuario no encontrado en la base de datos.'}

#Devolver una lista de usuarios
def listUsers():
    #Leemos todos los usuarios del contenedor
    users = container.read_all_items()

    return [User(**user) for user in users]

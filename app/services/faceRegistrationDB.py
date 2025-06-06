import os
from dotenv import load_dotenv
from azure.cosmos import CosmosClient
from app.models.registration import FaceRegistration

#Cargar las variables de entorno desde el archivo .env
load_dotenv()

#Variables de entorno
COSMOS_URL = os.getenv('COSMOS_URL')
COSMOS_KEY = os.getenv('COSMOS_KEY')
DATABASE_NAME = os.getenv('DATABASE_NAME')
FACES_CONTAINER_NAME = os.getenv('FACES_CONTAINER_NAME', 'faces_registration')

#Validamos que las variables de entorno necesarias esten definidas
if not COSMOS_URL or not COSMOS_KEY or not DATABASE_NAME or not FACES_CONTAINER_NAME:
    raise ValueError('Las variables de entorno COSMOS_URL, COSMOS_KEY, DATABASE_NAME y FACES_CONTAINER_NAME son necesarias.')

#Crear cliente de cosmos
client = CosmosClient(COSMOS_URL, credential = COSMOS_KEY)
db = client.get_database_client(DATABASE_NAME)
container = db.get_container_client(FACES_CONTAINER_NAME)

#Crear un usuario en la base de datos
def createFaceRegistration(face_registration: FaceRegistration):
    try:
        #Creamos el registro de cara en la base de datos
        return True, container.create_item(face_registration.model_dump())
    
    except Exception as e:
        return (False, str(e))

#Leer registros de cara por ID
def getFaceRegisterByUserId(user_id: str):
    try:
        #Buscamos los registros de cara por userID
        user_face_registration = container.read_item(user_id, partition_key = user_id)
        return True, FaceRegistration(**user_face_registration).model_dump()

    except Exception as e:
        return False, str(e)

#Borrar un registro de rostro por ID
def deleteUserById(face_register_id: str):
    try:
        #Borramos el usuario por ID
        return True, container.delete_item(face_register_id, partition_key = face_register_id)
    
    except Exception as e:
        return False, str(e)

#Devolver una lista de rostros registrados
def listFacesRegister():
    try:
        #Leemos todos los usuarios del contenedor
        faces_register = container.read_all_items()
        return True, [FaceRegistration(**face_register).model_dump() for face_register in faces_register]

    except Exception as e:
        return False, str(e)
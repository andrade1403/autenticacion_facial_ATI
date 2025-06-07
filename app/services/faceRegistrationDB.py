from datetime import datetime
from app.models.registration import FaceRegistration

class FaceRegistrationCRUDService:
    def __init__(self, container):
        self.container = container

    def createFaceRegistrationDB(self, face_registration: FaceRegistration):
        try:
            #Convertimos el usuario a un diccionario
            face_dict = face_registration.model_dump()
            
            #Ponemos fecha como string
            face_dict['fechaRegistro'] = datetime.strftime(face_dict['fechaRegistro'], '%Y-%m-%d')

            #Creamos el registro de cara en la base de datos
            return True, self.container.create_item(face_dict)
        
        except Exception as e:
            return False, str(e)

    def getFaceRegisterByUserIdDB(self, user_id: str):
        try:
            #Buscamos los registros de cara por ID de usuario
            query = 'SELECT * FROM c WHERE c.userId = @userId'
            parameters = [{'name': '@userId', 'value': user_id}]

            #Ejecutamos la consulta
            items = list(self.container.query_items(
                query = query,
                parameters = parameters,
                enable_cross_partition_query = True
            ))

            return True, FaceRegistrationCRUDService.parseFaceRegistration(items) if items else 'No hay registros de cara para este usuario'

        except Exception as e:
            return False, str(e)

    def deleteFaceRegisterByIdDB(self, face_register_id: str):
        try:
            #Borramos el usuario por ID
            return True, self.container.delete_item(face_register_id, partition_key = face_register_id)
        
        except Exception as e:
            return False, str(e)

    def listFacesRegister(self):
        try:
            #Leemos todos los usuarios del contenedor
            faces = self.container.read_all_items()
            return True, FaceRegistrationCRUDService.parseFaceRegistration(faces)

        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def parseFaceRegistration(faces: list):
        try:
            #Creamos una lista de objetos FaceRegistration
            face_objs = []

            for face in faces:
                #Crear objeto FaceRegistration y convertirlo a dict
                face_obj = FaceRegistration(**face)
                face_dict = face_obj.model_dump()

                #Convertir fechaRegistro a str
                face_dict['fechaRegistro'] = face_obj.fechaRegistro.strftime('%Y-%m-%d')
                face_objs.append(face_dict)
            
            return face_objs
        
        except Exception as e:
            return False, str(e)
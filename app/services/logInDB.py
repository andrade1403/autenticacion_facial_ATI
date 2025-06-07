from datetime import datetime
from app.models.login import LogIn

class LogInCRUDService:
    def __init__(self, container):
        self.container = container

    def createLogInDB(self, login: LogIn):
        try:
            #Convertimos el login a un diccionario
            login_dict = login.model_dump()
            
            #Ponemos fecha como string
            login_dict['fechaLogIn'] = datetime.strftime(login_dict['fechaLogIn'], '%Y-%m-%d')

            #Creamos el login en la base de datos
            return True, self.container.create_item(login_dict)
        
        except Exception as e:
            return False, str(e)

    def getLogInByUserIdDB(self, user_id: str):
        try:
            #Buscamos los logins por ID de usuario
            query = 'SELECT * FROM c WHERE c.userId = @userId'
            parameters = [{'name': '@userId', 'value': user_id}]

            #Ejecutamos la consulta
            items = list(self.container.query_items(
                query = query,
                parameters = parameters,
                enable_cross_partition_query = True
            ))

            return True, LogInCRUDService.parseFaceRegistration(items) if items else 'No hay registros de cara para este usuario'

        except Exception as e:
            return False, str(e)

    def listLogIns(self):
        try:
            #Leemos todos los logins del contenedor
            faces = self.container.read_all_items()
            return True, LogInCRUDService.parseFaceRegistration(faces)

        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def parseFaceRegistration(faces: list):
        try:
            #Creamos una lista de objetos LogIn
            face_objs = []

            for face in faces:
                #Crear objeto LogIn y convertirlo a dict
                face_obj = LogIn(**face)
                face_dict = face_obj.model_dump()

                #Convertir fechaRegistro a str
                face_dict['fechaLogIn'] = face_obj.fechaLogIn.strftime('%Y-%m-%d')
                face_objs.append(face_dict)
            
            return face_objs
        
        except Exception as e:
            return False, str(e)
from app.models.registration import FaceRegistration

class FaceRegistrationCRUDService:
    def __init__(self, container):
        self.container = container

    def createFaceRegistrationDB(self, face_registration: FaceRegistration):
        try:
            #Creamos el registro de cara en la base de datos
            return True, self.container.create_item(face_registration.model_dump())
        
        except Exception as e:
            return False, str(e)

    def getFaceRegisterByUserIdDB(self, user_id: str):
        try:
            #Buscamos los registros de cara por userID
            user_face_registration = self.container.read_item(user_id, partition_key = user_id)
            return True, FaceRegistration(**user_face_registration).model_dump()

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
            faces_register = self.container.read_all_items()
            print([FaceRegistration(**face).model_dump() for face in faces_register])
            return True, [FaceRegistration(**face).model_dump() for face in faces_register]

        except Exception as e:
            return False, str(e)
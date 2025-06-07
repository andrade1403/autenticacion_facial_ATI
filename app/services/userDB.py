from app.models.users import User

class UserCRUDService:
    def __init__(self, container):
        self.container = container

    def createUserDB(self, user: User):
        try:
            #Creamos el usuario en la base de datos
            return True, self.container.create_item(user.model_dump())
        
        except Exception as e:
            return False, str(e)

    def getUserByIdDB(self, user_id: str):
        try:
            #Buscamos el usuario por ID
            user = self.container.read_item(user_id, partition_key = user_id)
            return True, User(**user).model_dump()

        except Exception as e:
            return False, str(e)

    def deleteUserByIdDB(self, user_id: str):
        try:
            #Borramos el usuario por ID
            return True, self.container.delete_item(user_id, partition_key = user_id)
        
        except Exception as e:
            return False, str(e)

    def listUsers(self):
        try:
            #Leemos todos los usuarios del contenedor
            users = self.container.read_all_items()
            return True, [User(**user).model_dump() for user in users]

        except Exception as e:
            return False, str(e)
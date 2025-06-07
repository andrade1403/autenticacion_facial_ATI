from app.utils.settings import Settings
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosResourceNotFoundError

class DBConnection:
    def __init__(self):
        Settings.validate()
        self.client = CosmosClient(Settings.COSMOS_URL, credential = Settings.COSMOS_KEY)
        self.db = self.client.get_database_client(Settings.DATABASE_NAME)
    
    def getContainer(self, container_name):
        try:
            #Intentamos obtener el contenedor
            container = self.db.get_container_client(container_name)

            #Forzamos una llamada para verificar si realmente existe
            container.read()

        except CosmosResourceNotFoundError:
            #Crea el contenedor si no existe
            container = self.db.create_container_if_not_exists(
                id = container_name,
                partition_key = PartitionKey(path = '/id')
            )
        
        return container
    
    def deleteContainer(self, container_name):
        try:
            #Intentamos eliminar el contenedor
            self.db.delete_container(container_name)
            return True, f'Contenedor {container_name} eliminado correctamente'
        
        except CosmosResourceNotFoundError:
            return False, f'El contenedor {container_name} no existe'
        
        except Exception as e:
            return False, str(e)
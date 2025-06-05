import os
from face_sdk import FaceEngine

#Ruta al archivo de configuración del modelo
CONFIG_PATH = os.path.join('configs', 'recognition_irse50.yaml')

#Crear una instancia global de FaceEngine y cargar el modelo
face_engine = FaceEngine(config_path = CONFIG_PATH)
face_engine.load_model()

#Funcion para extraer el vector de embedding de una imagen o video
def extractEmbedding(archivo):
    try:
        #Extraer el vector de embedding de la imagen o video
        embedding = face_engine.get_embedding(archivo)

        #Validar si se obtuvo un embedding valido
        if embedding is None or embedding.shape[0] == 0:
            return False, 'No se detectó un rostro en la imagen o video'

        return True, embedding.tolist()
    
    except Exception as e:
        return False, f'Error al procesar imagen o video: {str(e)}'

import yaml
import numpy as np
from face_sdk.core.model_loader.face_detection.FaceDetModelLoader import FaceDetModelLoader
from face_sdk.core.model_handler.face_detection.FaceDetModelHandler import FaceDetModelHandler
from face_sdk.core.model_loader.face_alignment.FaceAlignModelLoader import FaceAlignModelLoader
from face_sdk.core.model_handler.face_alignment.FaceAlignModelHandler import FaceAlignModelHandler
from face_sdk.core.image_cropper.arcface_cropper.FaceRecImageCropper import FaceRecImageCropper
from face_sdk.core.model_loader.face_recognition.FaceRecModelLoader import FaceRecModelLoader
from face_sdk.core.model_handler.face_recognition.FaceRecModelHandler import FaceRecModelHandler

#Cargar configuraciones de modelos
def loadModelConfig(scene = 'non-mask'):
    #Abrimos el archivo de configuracion de modelos
    with open('face_sdk/config/model_conf.yaml') as f:
        model_conf = yaml.safe_load(f)

    return model_conf[scene]

#Inicializar modelos
model_path = 'models'
config = loadModelConfig()

#Cargar modelo de deteccion
faceDetModelLoader = FaceDetModelLoader(model_path, 'face_detection', config['face_detection'])
det_model, det_cfg = faceDetModelLoader.load_model()
faceDetModelHandler = FaceDetModelHandler(det_model, 'cuda:0', det_cfg)

#Cargar modelo de alineamiento
faceAlignModelLoader = FaceAlignModelLoader(model_path, 'face_alignment', config['face_alignment'])
align_model, align_cfg = faceAlignModelLoader.load_model()
faceAlignModelHandler = FaceAlignModelHandler(align_model, 'cuda:0', align_cfg)

#Cargar modelo de reconocimiento
faceRecModelLoader = FaceRecModelLoader(model_path, 'face_recognition', config['face_recognition'])
rec_model, rec_cfg = faceRecModelLoader.load_model()
faceRecModelHandler = FaceRecModelHandler(rec_model, 'cuda:0', rec_cfg)

#Carga modelo de recorte de imagen
face_cropper = FaceRecImageCropper()

def extractEmbedding(archivo, score_threshold = 0.85):
    try:
        #Deteccion de rostro
        dets = faceDetModelHandler.inference_on_image(archivo)
        if dets is None or len(dets) == 0:
            return False, 'No se detectó ningún rostro'

        #Seleccionamos la detección con mayor score
        best_box = max(dets, key = lambda b: b[4])

        #Validamos si el score de la mejor detección es menor al umbral
        if best_box[4] < score_threshold:
            return False, 'Confianza de detección por debajo del umbral'

        #Alineamiento
        landmarks = faceAlignModelHandler.inference_on_image(archivo, best_box)

        #Validamos si se obtuvieron los landmarks
        if landmarks is None or landmarks.shape != (5, 2):
            return False, 'No se pudieron obtener los landmarks'

        #Lista de coordenadas de landmarks
        landmarks_list = [coord for point in landmarks.astype(np.int32) for coord in point]

        #Recorte alineado
        cropped_image = face_cropper.crop_image_by_mat(archivo, landmarks_list)

        #Validamos si el recorte fue exitoso
        if cropped_image is None:
            return False, 'Error al recortar la imagen'

        #Extraccion de embeddings
        feature = faceRecModelHandler.inference_on_image(cropped_image)

        #Validamos si se obtuvo el embedding
        if feature is None or feature.shape[0] == 0:
            return False, 'Error al extraer el embedding'

        return True, feature.tolist()

    except Exception as e:
        return False, f'Error en el procesamiento facial: {str(e)}'

def compareEmbeddings(embedding_1, embedding_2):
    #Validamos que los embeddings no sean nulos
    if embedding_1 is None or embedding_2 is None:
        return False, 'Uno o ambos embeddings son nulos'
    
    #Transformar las listas de embeddings a arreglos de numpy y calcular la similitud coseno
    a = np.array(embedding_1)
    b = np.array(embedding_2)

    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
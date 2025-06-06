import cv2 as cv 
import numpy as np 
import os

# Ruta del dataset de imágenes faciales
dataSet = r'C:\Users\DELL\Documents\Universidad\CARRERA ISC ITM\NOVENO SEMESTRE\IA\phyton\datasets\caras'
faces = os.listdir(dataSet)
print("Carpetas encontradas:", faces)

labels = []    # Etiquetas numéricas para cada persona
facesData = [] # Imágenes faciales en escala de grises
label = 0      # Índice que identifica a cada persona

# Definir el tamaño fijo para las imágenes (por ejemplo, 100x100 píxeles)
fixed_width = 100
fixed_height = 100

for face in faces:
    facePath = os.path.join(dataSet, face)
    # Lista los archivos en la carpeta de cada persona
    for faceName in os.listdir(facePath):
        imgPath = os.path.join(facePath, faceName)
        # Cargar la imagen en escala de grises
        img = cv.imread(imgPath, cv.IMREAD_GRAYSCALE)
        if img is None:
            print("No se pudo cargar la imagen:", imgPath)
            continue
        # Redimensionar la imagen al tamaño fijo
        img = cv.resize(img, (fixed_width, fixed_height))
        facesData.append(img)
        labels.append(label)
    label += 1

print("Número de imágenes de la primera persona:", np.count_nonzero(np.array(labels)==0))

# Crear y entrenar el reconocedor usando el algoritmo Fisherfaces
faceRecognizer = cv.face.FisherFaceRecognizer_create()
faceRecognizer.train(facesData, np.array(labels))
faceRecognizer.write('FacesFisherFace.xml')
print("Modelo guardado en 'FacesFisherFace.xml'")

#1 sola clase
#faceRecognizer = cv.face.LBPHFaceRecognizer_create()
#faceRecognizer.train(facesData, np.array(labels))
#faceRecognizer.write('laloLBPHFace.xml')

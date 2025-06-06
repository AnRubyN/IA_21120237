import cv2 as cv
import numpy as np
import os
from tqdm import tqdm # Importar tqdm
import time # Opcional: para medir el tiempo de entrenamiento

# Ruta del dataset de imágenes faciales
dataSet = r'C:\Users\DELL\Documents\Universidad\CARRERA ISC ITM\NOVENO SEMESTRE\IA\phyton\datasets\caras'

print("Calculando el número total de imágenes...")
total_images = 0
faces = [] # Guardaremos las carpetas válidas aquí
allowed_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.pgm') # Extensiones de imagen permitidas

# Primero asegurarnos que los items en dataSet son directorios
potential_faces = os.listdir(dataSet)
for face_folder_name in potential_faces:
    face_folder_path = os.path.join(dataSet, face_folder_name)
    if os.path.isdir(face_folder_path): # Solo procesar si es una carpeta
        faces.append(face_folder_name) # Añadir a la lista de carpetas de caras válidas
        for filename in os.listdir(face_folder_path):
            if filename.lower().endswith(allowed_extensions):
                total_images += 1
    else:
         print(f"-> Advertencia: Se omitió '{face_folder_name}' porque no es una carpeta.")


print(f"Se encontraron {len(faces)} carpetas de personas.")
print(f"Total de imágenes a procesar: {total_images}")

if total_images == 0:
    print("¡Error! No se encontraron imágenes válidas en las carpetas especificadas. Saliendo.")
    exit() # Salir si no hay imágenes

# --- PASO 2: Procesar imágenes con barra de progreso ---
labels = []    # Etiquetas numéricas para cada persona
facesData = [] # Imágenes faciales en escala de grises
label = 0      # Índice que identifica a cada persona

# Definir el tamaño fijo para las imágenes
fixed_width = 100
fixed_height = 100

print("\nIniciando carga y preprocesamiento de imágenes...")
# Usar tqdm para la barra de progreso general sobre el total de imágenes
# Nota: tqdm se actualizará manualmente dentro del bucle
with tqdm(total=total_images, desc="Progreso General", unit="img") as pbar_general:
    for face in faces: # Iterar sobre las carpetas de personas validadas
        facePath = os.path.join(dataSet, face)
        print(f"\nProcesando carpeta: {face} (Persona ID: {label})") # Indica qué persona se procesa

        # Listar archivos válidos para esta persona
        person_files = []
        for faceName in os.listdir(facePath):
             if faceName.lower().endswith(allowed_extensions):
                 person_files.append(faceName)

        # Iterar sobre los archivos de imagen de esta persona
        # (Opcional) Podrías añadir un tqdm aquí también si quieres una barra por persona:
        # for faceName in tqdm(person_files, desc=f"Imágenes de {face}", leave=False):
        for faceName in person_files:
            imgPath = os.path.join(facePath, faceName)
            # Cargar la imagen en escala de grises
            img = cv.imread(imgPath, cv.IMREAD_GRAYSCALE)

            if img is None:
                print(f"\n -> ADVERTENCIA: No se pudo cargar la imagen: {imgPath}")
                # No actualizamos la barra si la imagen falla, ya que se contó al inicio
                # Podrías descontar de total_images si quieres ser más preciso aquí
                continue

            # Redimensionar la imagen al tamaño fijo
            img_resized = cv.resize(img, (fixed_width, fixed_height))
            facesData.append(img_resized)
            labels.append(label)

            # Actualizar la barra de progreso general
            pbar_general.update(1)

        label += 1 # Incrementar etiqueta DESPUÉS de procesar todas las imágenes de una persona

print("\nCarga y preprocesamiento de imágenes completado.")
print(f"Total imágenes cargadas: {len(facesData)}")
print(f"Total etiquetas generadas: {len(labels)}")
print("Número de imágenes de la primera persona (label 0):", np.count_nonzero(np.array(labels)==0))


# --- PASO 3: Entrenar con indicación ---
if not facesData:
     print("¡Error Crítico! No hay datos de imágenes para entrenar.")
else:
    print("\nIniciando entrenamiento del modelo Fisherfaces...")
    start_time = time.time() # Opcional: medir tiempo

    # Crear y entrenar el reconocedor usando el algoritmo Fisherfaces
    faceRecognizer = cv.face.FisherFaceRecognizer_create()
    faceRecognizer.train(facesData, np.array(labels))

    end_time = time.time() # Opcional: medir tiempo
    print(f"Entrenamiento completado en {end_time - start_time:.2f} segundos.") # Opcional

    # Guardar el modelo
    model_filename = 'FacesFisherFace.xml'
    faceRecognizer.write(model_filename)
    print(f"Modelo guardado en '{model_filename}'")

# --- Código LBPH comentado (sin cambios) ---
#print("\nEntrenando modelo LBPH...")
#faceRecognizerLBPH = cv.face.LBPHFaceRecognizer_create()
#faceRecognizerLBPH.train(facesData, np.array(labels))
#model_filename_lbph = 'laloLBPHFace.xml'
#faceRecognizerLBPH.write(model_filename_lbph)
#print(f"Modelo LBPH guardado en '{model_filename_lbph}'")
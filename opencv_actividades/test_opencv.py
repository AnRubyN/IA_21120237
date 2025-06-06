import cv2

# Imprimir versión
print("Versión de OpenCV:", cv2.__version__)

# Lee una imagen (asegúrate de que image.jpg exista en la carpeta)
img = cv2.imread("image.jpeg")

if img is not None:
    print("Imagen leída correctamente con OpenCV")
else:
    print("No se pudo leer la imagen")

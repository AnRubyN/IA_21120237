# Manejo eficiente de matrices e imagenes
import numpy as np
#Uasada para el procesamiento de video e imagenes
import cv2 as cv
import math 

rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
cap = cv.VideoCapture(0)
i = 0  
while True:
    ret, frame = cap.read() #ret indica si se ha leido correcatmanete y frame es la iamgen o fotograma actual
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)  #convierte a escala de grises
    rostros = rostro.detectMultiScale(gray, 1.3, 5) # color y precision
    for(x, y, w, h) in rostros:     # (x, y): esquina superior izquierda del rectángulo. (w, h): ancho y alto del rectángulo.
       #frame = cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
       frame2 = frame[ y:y+h, x:x+w] # Recorta únicamente el área del rostro del fotograma original usando las coordenadas detectadas.
       frame3 = frame[x+30:x+w-30, y+30:y+h-30]
       frame2 = cv.resize(frame2, (100, 100), interpolation=cv.INTER_AREA) # Redimensiona la imagen del rostro recortado a un tamaño fijo de 100x100 píxeles usando la interpolación INTER_AREA (buena calidad al reducir imágenes).
       #cv.imwrite('/home/likcos/recorte/lalo'+str(i)+'.jpg', frame)
       cv.imwrite('C:/Users/DELL/Documents/Universidad/CARRERA ISC ITM/NOVENO SEMESTRE/IA/phyton/images'+str(i)+'.jpg', frame2) #Guarda la imagen recortada del rostro en la carpeta
       cv.imshow('rostror', frame2) #Muestra en tiempo real una ventana titulada 'rostror' con la imagen recortada del rostro que acaba de guardar.
    cv.imshow('rostros', frame)
    i = i+1
    k = cv.waitKey(1)
    if k == 27:
        break
cap.release() #Libera los recursos del archivo de video usado (cap).
cv.destroyAllWindows() #Cierra todas las ventanas de visualización abiertas por OpenCV.
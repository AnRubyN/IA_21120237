import cv2 as cv
import os 

faces = ['arce', 'axel', 'curi', 'gerardo', 'ruby'] 
faceRecognizer = cv.face.LBPHFaceRecognizer_create() # LBPHFaceRecognizer_create():
faceRecognizer.read('FacesFisherFace.xml') #  Cargar modelo previamente entrenado desde el archivo XML laloLBPHFace.xml.


cap = cv.VideoCapture(0) #Abre la webcam para captura en vivo
rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml') #Carga el detector de rostros tipo Haar Cascade para detección frontal de rostros.


while True:
    ret, frame = cap.read() # Captura continuamente imágenes (frames) desde la webcam.
    if ret == False: break #Si falla la captura (ret==False), el bucle termina inmediatamente.
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) #Convierte la imagen capturada a escala de grises para facilitar detección y reconocimiento facial.
    cpGray = gray.copy() #Crea una copia de la imagen en gris para trabajar sobre ella.
    rostros = rostro.detectMultiScale(gray, 1.3, 3) #Detecta los rostros presentes en la imagen usando el clasificador Haar.
    #1.3: factor de escala (reduce imagen en cada iteración un 30%).
    #3: número mínimo de vecinos para considerar que realmente es un rostro.

    for(x, y, w, h) in rostros:
        frame2 = cpGray[y:y+h, x:x+w] #Recorre todos los rostros detectados.
        frame2 = cv.resize(frame2,  (100,100), interpolation=cv.INTER_CUBIC) #redimenciona el rostro a 100x100px
        result = faceRecognizer.predict(frame2) #Usa el reconocedor LBPH para predecir la identidad del rostro recortado y retorna una tupla result:
        #result[0]: Etiqueta numérica (persona identificada).
        #result[1]: Nivel de confianza (valor bajo implica alta confianza).
        cv.putText(frame, '{}'.format(result), (x,y-20), 1,3.3, (255,255,0), 1, cv.LINE_AA) #Escribe la etiqueta numérica y nivel de confianza encima del rostro (útil para pruebas).
        
        if result[1] < 70:
            #Si la confianza es alta (result[1] < 70):
            cv.putText(frame,'{}'.format(faces[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv.LINE_AA) #etiqueta con el nombre
            cv.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2) #dibuja rectangulo verde
        else:
            #Si la confianza es baja (result[1] >= 70):
            cv.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv.LINE_AA) #etiqueta desconocido
            cv.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2) #dibuja rectangulo rojo

    cv.imshow('frame', frame) #Muestra continuamente la imagen procesada en tiempo real en una ventana llamada "frame".
    k = cv.waitKey(1)
    if k == 27:
        break
#Libera la cámara y cierra todas las ventanas abiertas por OpenCV.
cap.release()
cv.destroyAllWindows()



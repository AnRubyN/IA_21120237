import cv2

#Cargar imagen 0 ➡(b/N) 1 ➡ color
img = cv2.imread ("image.jpg", 1)
b,g,r = cv2.split(img)
#img2 = cv2.imread ("image.jpeg", 0)

#canales de colores (1 canal = 1 matriz)
#img3 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#img4 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# mostrar la ventana con nombre 'salida' y con la img
cv2.imshow('salida', img)
cv2.imshow('salida1', b)
cv2.imshow('salida2', g)
cv2.imshow('salida3', r)

#Detener el- proceso de que se cieere la ventana
cv2.waitKey(0)

#Poder cerrar la ventana
cv2.destroyAllWindows()
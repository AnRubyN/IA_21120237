import joblib 
import numpy as np

# Cargar el modelo y el scaler
mlp_loaded = joblib.load('mlp_model.pkl')
scaler_loaded = joblib.load('scaler.pkl')

# Nuevo dato (4 caracteristicas como en el dataset Iris)
nuevo_dato=np.array([[5.1,3.5,1.4,0.2]])

# Normalizar el nuevo dato
nuevo_dato_escalado = scaler_loaded.transform(nuevo_dato)

# Hacer la prediccion
prediccion = mlp_loaded.predict(nuevo_dato_escalado)

# Diccionario para interpretar la clase
clases = {0: 'Setosa', 1: 'Versicolore', 2: 'Virginica'}


print(f'La flor pertenece a la clase: {clases[prediccion[0]]}')

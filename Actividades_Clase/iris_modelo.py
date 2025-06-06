# Libreria JobLib -> Guardar y cargar modelos 
# parametros: modelo entrenado y scalers

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

# cargar el data set iris
iris = load_iris()
X, y = iris.data, iris.target 

# Dividir eñ conjunto de netrenamiento y prueba (80%-20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Normalizar las caracteristicas (importante para MLP)
scaler = StandardScaler();
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Definir la red neuronal con una capa oculta de 10 neuronas
mlp = MLPClassifier(hidden_layer_sizes=(10,), activation='relu', solver='adam',mas_iter=500, random_state=42)

# Entrenar el modelo
mlp.fit (X_train, y_train)

# Hacer predicciones
y_pred = mlp.predict(X_test)

# Evaluar modelo
accuracy = accuracy_score(y_test, y_pred)
print(f'\Precisión en test: {accuracy:.4f}')
print(y_pred)
print(X_test)


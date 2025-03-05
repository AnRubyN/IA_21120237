# Modelar una red neuronal que pueda jugar al 5 en liena sin gravedad en un tablero de 20 * 20

## Tipo de Red Neuronal
**Red Neuronal Modular** que constara de los siguientes modulos:
* Un modulo para las secuencias horizontales
* Un modulo para las secuencias verticales
* Un modulo para las diagonales (ascendente y descendente)

## Definir los patrones a utilizar:


## Definirla funcion de activacion: 
* **Capas ocultas**: ReLU
* **Capas de Salida**: Sigmoide (2 salidas)

## Definir numero maximo de entrada: 2
* **Estado**: Indica si unac celda está vacía, ocupada por el jugador 1 o por el jugador 2.
* **Movimiento** : En que posición se espera o es más adecuando colocar la ficha en el siguiente movimiento

## Valores esperados a la salida de la red que s epueden esperar
* **[1]** : Ha conectado 5 en linea
* **[0]** : No ha conectado 5 en linea

## Valores maximos que puede tener el BIAS:
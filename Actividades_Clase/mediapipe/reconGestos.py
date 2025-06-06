import cv2
import mediapipe as mp
import numpy as np
import json
import os

# Inicializar el modelo de detección de malla facial de MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Abrir cámara para capturar video
cap = cv2.VideoCapture(0)

# Selección de landmarks clave (ojos, boca, nariz, cejas y párpados)
selected_points = [33, 133, 362, 263, 61, 291, 48, 278, 105, 334, 159, 386, 145, 374]
json_path = "data.json"

# Cargar datos guardados previamente de personas reconocidas
if os.path.exists(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
else:
    data = []

# Función para calcular distancia euclidiana entre dos puntos
def distancia(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

# Compara dos listas de distancias normalizadas para saber si son suficientemente similares
def comparar_distancias(dist_actual, dist_guardadas, umbral=0.2):
    errores = [abs(a - b) for a, b in zip(dist_actual, dist_guardadas)]
    return (sum(errores) / len(errores)) < umbral

# Clasificación de emociones basada en distancias normalizadas
def detectar_emocion_normalizada(d_boca_n, apertura_ojos_n, prom_cejas_n):
    # Reglas heurísticas basadas en relaciones geométricas
    if d_boca_n > 1.7 and prom_cejas_n > 0.8:
        return "Sorpresa"
    elif d_boca_n > 1.0 and apertura_ojos_n > 0.35 and prom_cejas_n > 0.45:
        return "Feliz"
    elif d_boca_n < 1.1 and apertura_ojos_n < 0.35 and prom_cejas_n < 0.6:
        return "Triste"
    elif 1.1 <= d_boca_n <= 1.6 and 0.3 <= apertura_ojos_n <= 0.45:
        return "Neutral"
    else:
        return "Indefinida"

# Bucle principal para leer frames y procesar
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Voltear imagen horizontalmente para efecto espejo
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar la imagen para detectar landmarks
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            puntos = {}

            # Extraer coordenadas X, Y de los landmarks seleccionados
            for idx in selected_points:
                x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                puntos[idx] = (x, y)
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)  # Visualización

            if all(idx in puntos for idx in selected_points):
                # Calcular distancias entre pares clave de puntos
                d_ojos_izq = distancia(puntos[362], puntos[263])
                d_ojos_der = distancia(puntos[33], puntos[133])
                d_boca = distancia(puntos[61], puntos[291])
                d_nariz = distancia(puntos[48], puntos[278])
                d_ceja_izq = distancia(puntos[105], puntos[159])
                d_ceja_der = distancia(puntos[334], puntos[386])
                d_apertura_ojos_izq = distancia(puntos[159], puntos[145])
                d_apertura_ojos_der = distancia(puntos[386], puntos[374])
                prom_apertura_ojos = (d_apertura_ojos_izq + d_apertura_ojos_der) / 2

                # Se define una referencia para normalizar las distancias (evita variación por cercanía)
                referencia = (d_ojos_izq + d_ojos_der) / 2

                # Normalización de cada distancia
                d_boca_n = d_boca / referencia
                d_ceja_izq_n = d_ceja_izq / referencia
                d_ceja_der_n = d_ceja_der / referencia
                prom_cejas_n = (d_ceja_izq_n + d_ceja_der_n) / 2
                apertura_ojos_n = prom_apertura_ojos / referencia

                # Vector final con medidas normalizadas
                dist_norm = [d_boca_n, d_ceja_izq_n, d_ceja_der_n, apertura_ojos_n]

                # Mostrar valores relevantes en pantalla para depuración visual
                cv2.putText(frame, f"Boca: {int(d_boca)}", (puntos[61][0], puntos[61][1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(frame, f"Cejas: {prom_cejas_n:.2f}", (30, 110),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 255), 2)
                cv2.putText(frame, f"Ojos: {apertura_ojos_n:.2f}", (30, 140),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 255, 200), 2)

                # Comparar con cada persona en base de datos
                nombre_reconocido = None
                for persona in data:
                    if comparar_distancias(dist_norm, persona["distancias"]):
                        nombre_reconocido = persona['nombre']
                        break

                # Mostrar el nombre si se reconoce
                if nombre_reconocido:
                    cv2.putText(frame, f"Reconocido: {nombre_reconocido}", (30, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                # Determinar emoción actual
                emocion = detectar_emocion_normalizada(d_boca_n, apertura_ojos_n, prom_cejas_n)
                color_emocion = {
                    "Feliz": (0, 255, 0),
                    "Sorpresa": (0, 255, 255),
                    "Triste": (180, 100, 255),
                    "Neutral": (200, 200, 200),
                    "Indefinida": (100, 100, 255)
                }.get(emocion, (255, 255, 0))

                # Mostrar emoción en pantalla
                cv2.putText(frame, f"Emocion: {emocion}", (30, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, color_emocion, 2)

                # Imprimir métricas para desarrollador
                print(f"Boca_n: {d_boca_n:.2f} | Cejas_n: {prom_cejas_n:.2f} | Ojos_n: {apertura_ojos_n:.2f}")

                # Guardar nueva entrada si el usuario presiona 's'
                key = cv2.waitKey(1) & 0xFF
                if key == ord('s'):
                    nombre = input("Nombre de la persona: ")
                    registro = {
                        "nombre": nombre,
                        "distancias": dist_norm
                    }
                    data.append(registro)
                    with open(json_path, "w") as f:
                        json.dump(data, f, indent=4)
                    print(f"✅ Datos guardados para {nombre}")

    # Mostrar la imagen procesada con la interfaz de resultados
    cv2.imshow('Reconocimiento de Gestos', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()

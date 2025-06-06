import cv2
import mediapipe as mp
import numpy as np
import json
import os

# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=2, 
                                  min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Captura de video
cap = cv2.VideoCapture(0)

# Lista de índices de landmarks específicos (ojos y boca y nariz)
selected_points = [33, 133, 362, 263, 61, 291, 48 , 278]  # Ojos y boca

# Ruta de archivo Json
json_path = "data.json"

# Cargar datos previos si existen
if os.path.exists(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
else:
    data = []

def distancia(p1, p2):
    """Calcula la distancia euclidiana entre dos puntos."""
    return np.linalg.norm(np.array(p1) - np.array(p2))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Espejo para mayor naturalidad
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            puntos = {}
            
            for idx in selected_points:
                x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                puntos[idx] = (x, y)
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)  # Dibuja el punto en verde
            
            # Calcular y mostrar distancia entre puntos (ejemplo: entre ojos)
            if 362 in puntos and 263 in puntos:
                d_ojos_izq = distancia(puntos[362 ], puntos[263])
                cv2.putText(frame, f"D_OjoL: {int(d_ojos_izq)}", (puntos[362][0], puntos[362][1] - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            # Calcular y mostrar distancia entre puntos (ejemplo: entre ojos)
            if 33 in puntos and 133 in puntos:
                d_ojos_derc = distancia(puntos[33], puntos[133])
                cv2.putText(frame, f"D_OjoR: {int(d_ojos_derc)}", (puntos[33][0], puntos[33][1] - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                
            # Calcular y mostrar distancia entre puntos (ejemplo: entre ojos)
            if 61 in puntos and 291 in puntos:
                d_boca = distancia(puntos[33], puntos[291])
                cv2.putText(frame, f"D_Boca: {int(d_boca)}", (puntos[61][0], puntos[61][1] - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                
            # Calcular y mostrar distancia entre puntos (ejemplo: entre ojos)
            if 48 in puntos and 278 in puntos:
                d_nariz = distancia(puntos[48], puntos[278])
                cv2.putText(frame, f"D_Nariz: {int(d_nariz)}", (puntos[48][0], puntos[48][1] - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
                # Guardar si se presiona 's'
                key = cv2.waitKey(1) & 0xFF
                if key == ord('s'):
                    nombre = input("Nombre de la persona: ")
                    registro = {
                        "nombre": nombre,
                        "distancias": [d_ojos_izq, d_ojos_derc, d_boca, d_nariz]
                    }
                    data.append(registro)
                    with open(json_path, "w") as f:
                        json.dump(data, f, indent=4)
                    print(f"✅ Datos guardados para {nombre}")

    cv2.imshow('PuntosFacialesMediaPipe', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
import pygame
import random
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
import numpy as np
import time

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego: Disparo de Bala, Salto, Nave y Menú")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Variables del jugador, bala, nave, fondo, etc.
jugador = None
bala = None
fondo = None
nave = None
menu = None

# Variables de salto
salto = False
salto_altura = 15
gravedad = 1
en_suelo = True

# --- NUEVAS VARIABLES PARA LA SEGUNDA BALA ---
bala2 = None
velocidad_bala2_y = 3 # Velocidad constante de caída
bala2_activa = False

# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False
modelo_elegido = None
modelos_entrenados = {1: False, 2: False, 3: False}
modelo = None

# --- NUEVAS VARIABLES PARA EL MODELO DE MOVIMIENTO HORIZONTAL ---
datos_modelo_horizontal = []
modelo_horizontal = None
modelos_entrenados_horizontal = {1: False, 2: False, 3: False}

# --- NUEVAS BANDERAS PARA CONTROLAR IMPRESIONES ÚNICAS ---
print_once_salto_trained = {1: False, 2: False, 3: False}
print_once_horizontal_trained = {1: False, 2: False, 3: False}

# Lista para guardar los datos de velocidad, distancia y salto (target)
datos_modelo = []

# Cargar las imágenes
try:
    jugador_frames = [
        pygame.image.load('assets/sprites/hk1.png'),
        pygame.image.load('assets/sprites/hk3.png'),
        pygame.image.load('assets/sprites/hk2.png')
    ]
    bala_img = pygame.image.load('assets/sprites/ballonh.png')
    bala_vertical_img = pygame.image.load('assets/sprites/ballon1.png')
    fondo_img = pygame.image.load('assets/game/fondohk.jpg')
    nave_img = pygame.image.load('assets/game/Tuxedo.png')
    menu_img = pygame.image.load('assets/game/menu.png')
except pygame.error as e:
    print(f"Error cargando imágenes: {e}")
    print("Asegúrate de que las rutas a 'assets/' son correctas y las imágenes existen.")
    pygame.quit()
    exit()

# Escalar la imagen de fondo para que coincida con el tamaño de la pantalla
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear el rectángulo del jugador y de las balas
# Usar el ancho y alto real del sprite del jugador y centrarlo
jugador = pygame.Rect(w // 2 - jugador_frames[0].get_width() // 2, h - 100, jugador_frames[0].get_width(), jugador_frames[0].get_height())
# DEBUG: Imprimir dimensiones del jugador para verificar
print(f"DEBUG: Dimensiones del sprite del jugador (hk1.png): {jugador_frames[0].get_width()}x{jugador_frames[0].get_height()}")
print(f"DEBUG: Dimensiones del Rect del jugador: {jugador.width}x{jugador.height}")

bala = pygame.Rect(w - 50, h - 90, bala_img.get_width(), bala_img.get_height())
nave = pygame.Rect(w - 100, h - 150, nave_img.get_width(), nave_img.get_height())
menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)

# --- INICIALIZAR LA SEGUNDA BALA ---
#  bala2.x se inicializa para apuntar al centro del jugador
bala2 = pygame.Rect(jugador.x + jugador.width // 2 - bala_vertical_img.get_width() // 2, -bala_vertical_img.get_height(), bala_vertical_img.get_width(), bala_vertical_img.get_height())
bala2_activa = True

# Variables para la animación del jugador
current_frame = 0
frame_speed = 10
frame_count = 0

# Variables para la bala
velocidad_bala = -10
bala_disparada = False

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w


# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-8, -5)
        bala_disparada = True


# Función para reiniciar la posición de la bala principal
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50
    bala_disparada = False


# Función para manejar el salto
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura
        salto_altura -= gravedad

        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15
            en_suelo = True


# Función para actualizar el juego
def update():
    global bala, velocidad_bala, current_frame, frame_count, fondo_x1, fondo_x2, modo_auto, bala2, velocidad_bala2_y, bala2_activa, jugador

    # Mover el fondo
    fondo_x1 -= 1
    fondo_x2 -= 1

    if fondo_x1 <= -w:
        fondo_x1 = w
    if fondo_x2 <= -w:
        fondo_x2 = w

    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))

    # Dibujar la nave
    pantalla.blit(nave_img, (nave.x, nave.y))

    # Mover y dibujar la bala principal
    if bala_disparada:
        bala.x += velocidad_bala
    if bala.x < 0:
        reset_bala()
    pantalla.blit(bala_img, (bala.x, bala.y))

    # --- MOVIMIENTO Y DIBUJO DE LA SEGUNDA BALA (NUEVO) ---
    if bala2_activa:
        # Bala vertical ya NO apunta al centro del personaje en cada frame.
        # Su posición X solo se establece al inicio o al reiniciar.
        bala2.y += velocidad_bala2_y
        pantalla.blit(bala_vertical_img, (bala2.x, bala2.y)) # Usar la nueva imagen para la bala vertical

        if bala2.y > h:
            # Al reiniciar, apunta al centro del jugador en ese momento.
            bala2.x = jugador.x + jugador.width // 2 - bala_vertical_img.get_width() // 2
            bala2.y = -bala_vertical_img.get_height()


    # Colisión entre la bala principal y el jugador
    if jugador.colliderect(bala):
        print("❗❗❗ Colisión detectada con bala principal ❗❗❗")
        reiniciar_juego()

    # --- COLISIÓN ENTRE LA SEGUNDA BALA Y EL JUGADOR (NUEVO) ---
    if jugador.colliderect(bala2):
        print("¡Colisión detectada con segunda bala!")
        reiniciar_juego()


# --- FUNCIÓN PARA GUARDAR DATOS DEL MODELO (NOW FOR BOTH MODELS) ---
def guardar_datos(current_keys):
    global jugador, bala, velocidad_bala, salto, datos_modelo, datos_modelo_horizontal
    
    # Datos para el modelo de SALTO
    distancia_horizontal_to_bullet1 = abs(jugador.x - bala.x)
    salto_hecho = 1 if salto else 0
    datos_modelo.append((abs(velocidad_bala), distancia_horizontal_to_bullet1, salto_hecho))

    # Datos para el modelo de MOVIMIENTO HORIZONTAL (NUEVO)
    horizontal_action = 1
    if current_keys[pygame.K_LEFT]:
        horizontal_action = 0
    elif current_keys[pygame.K_RIGHT]:
        horizontal_action = 2

    datos_modelo_horizontal.append((abs(velocidad_bala), distancia_horizontal_to_bullet1, horizontal_action))


# Función para pausar el juego
def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        print("Juego pausado.")
        if not modo_auto:
            print("✅ Datos registrados en modo manual para Salto:", datos_modelo)
            print("✅ Datos registrados en modo manual para Movimiento Horizontal:", datos_modelo_horizontal)
    else:
        print("Juego reanudado.")


# Función para mostrar el menú y seleccionar el modo de juego
def mostrar_menu():
    global menu_activo, modo_auto, modelo_elegido, modelos_entrenados, datos_modelo, modelo, datos_modelo_horizontal, modelos_entrenados_horizontal
    print(">>> Entrando a mostrar_menu().")
    pantalla.fill(NEGRO)
    menu_texto = [
        "Presiona:",
        "'1' para Vecinos Cercanos (KV)",
        "'2' para Árbol de Decisión (AD)",
        "'3' para Red Neuronal (RN)",
        "'M' para Modo Manual (recolectar datos)",
        "'Q' para Salir"
    ]
    for i, linea in enumerate(menu_texto):
        texto_renderizado = fuente.render(linea, True, BLANCO)
        pantalla.blit(texto_renderizado, (w // 4, h // 4 + i * fuente.get_linesize()))

    # Mostrar modelos ya entrenados con los datos actuales
    texto_modelos_entrenados_salto = "Modelos Salto Entrenados: "
    modelos_str_salto = []
    for i in range(1, 4):
        if modelos_entrenados[i]:
            if i == 1: modelos_str_salto.append("KNN")
            elif i == 2: modelos_str_salto.append("AD")
            elif i == 3: modelos_str_salto.append("RN")
    texto_modelos_entrenados_salto += ", ".join(modelos_str_salto) if modelos_str_salto else "Ninguno"
    pantalla.blit(fuente.render(texto_modelos_entrenados_salto, True, BLANCO), (w // 4, h // 4 + len(menu_texto) * fuente.get_linesize() + 10))

    texto_modelos_entrenados_horizontal = "Modelos Mov. Horizontal Entrenados: "
    modelos_str_horizontal = []
    for i in range(1, 4):
        if modelos_entrenados_horizontal[i]:
            if i == 1: modelos_str_horizontal.append("KNN")
            elif i == 2: modelos_str_horizontal.append("AD")
            elif i == 3: modelos_str_horizontal.append("RN")
    texto_modelos_entrenados_horizontal += ", ".join(modelos_str_horizontal) if modelos_str_horizontal else "Ninguno"
    pantalla.blit(fuente.render(texto_modelos_entrenados_horizontal, True, BLANCO), (w // 4, h // 4 + len(menu_texto) * fuente.get_linesize() + 40))


    # Mostrar cantidad de datos disponibles
    #texto_datos_salto = f"Datos Salto: {len(datos_modelo)} registros."
    #pantalla.blit(fuente.render(texto_datos_salto, True, BLANCO), (w // 4, h // 4 + (len(menu_texto) + 1) * fuente.get_linesize() + 70))
    #texto_datos_horizontal = f"Datos Mov. Horizontal: {len(datos_modelo_horizontal)} registros."
    #pantalla.blit(fuente.render(texto_datos_horizontal, True, BLANCO), (w // 4, h // 4 + (len(menu_texto) + 2) * fuente.get_linesize() + 80))


    pygame.display.flip()
    print(">>> Menú mostrado. Esperando selección...")

    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                print("Saliendo del juego desde el menú (Evento QUIT).")
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                print(f"DEBUG: Tecla presionada en menú: {evento.key}")
                # MODIFICACIÓN: Imprimir datos completos al presionar tecla 'v' o 'V'
                if evento.key == pygame.K_v: # Comprobar si la tecla 'v' fue presionada
                    print("\n---------------- CONTENIDO DE DATOS DE ENTRENAMIENTO ---------------")
                    print(f"DATOS SALTO ({len(datos_modelo)} registros): {str(datos_modelo)}")
                    print(f"\nDATOS MOVIMIENTO HORIZONTAL ({len(datos_modelo_horizontal)} registros): {str(datos_modelo_horizontal)}")
                    print("-------------------------------------------\n")
                
                min_data_needed = 10
                action_taken = False
                if evento.key == pygame.K_1:
                    if len(datos_modelo) < min_data_needed or len(datos_modelo_horizontal) < min_data_needed:
                        print(f"Advertencia: No hay suficientes datos (Salto: {len(datos_modelo)}, Mov. Horiz.: {len(datos_modelo_horizontal)}) para entrenar los modelos con KNN. Juegue en Modo Manual ('M').")
                    modelo_elegido = 1
                    modo_auto = True
                    menu_activo = False
                    action_taken = True
                    print("Modo automático: Vecinos Cercanos (KNN) seleccionado para AMBAS IAs.")
                elif evento.key == pygame.K_2:
                    if len(datos_modelo) < min_data_needed or len(datos_modelo_horizontal) < min_data_needed:
                            print(f"Advertencia: No hay suficientes datos (Salto: {len(datos_modelo)}, Mov. Horiz.: {len(datos_modelo_horizontal)}) para entrenar los modelos con Árbol de Decisión. Juegue en Modo Manual ('M').")
                    modelo_elegido = 2
                    modo_auto = True
                    menu_activo = False
                    action_taken = True
                    print("Modo automático: Árbol de Decisión seleccionado para AMBAS IAs.")
                elif evento.key == pygame.K_3:
                    if len(datos_modelo) < min_data_needed or len(datos_modelo_horizontal) < min_data_needed:
                            print(f"Advertencia: No hay suficientes datos (Salto: {len(datos_modelo)}, Mov. Horiz.: {len(datos_modelo_horizontal)}) para entrenar los modelos con Red Neuronal. Juegue en Modo Manual ('M').")
                    modelo_elegido = 3
                    modo_auto = True
                    menu_activo = False
                    action_taken = True
                    print("Modo automático: Red Neuronal seleccionado para AMBAS IAs.")
                elif evento.key == pygame.K_m:
                    modo_auto = False
                    menu_activo = False
                    action_taken = True
                    print("Reiniciando datasets y modelos para una nueva sesión manual.")
                    datos_modelo.clear()
                    datos_modelo_horizontal.clear()
                    modelos_entrenados = {1: False, 2: False, 3: False}
                    modelos_entrenados_horizontal = {1: False, 2: False, 3: False}
                    modelo = None
                    modelo_horizontal = None
                    global print_once_salto_trained, print_once_horizontal_trained
                    print_once_salto_trained = {1: False, 2: False, 3: False}
                    print_once_horizontal_trained = {1: False, 2: False, 3: False}
                    print(f"Datos de entrenamiento actuales (Salto): {len(datos_modelo)} registros.")
                    print(f"Datos de entrenamiento actuales (Mov. Horizontal): {len(datos_modelo_horizontal)} registros.")
                elif evento.key == pygame.K_q:
                    print("Saliendo del juego desde el menú (Tecla Q).")
                    pygame.quit()
                    exit()
                
                if action_taken and not menu_activo:
                    print(">>> Saliendo de mostrar_menu() para iniciar el juego.")
                    pass

        pygame.time.delay(100)
    print(">>> mostrar_menu() finalizado (menu_activo es False).")


# Función para reiniciar el juego tras la colisión
def reiniciar_juego():
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo, modelo_elegido, modelos_entrenados, modelo, bala2, bala2_activa, datos_modelo_horizontal, modelo_horizontal, modelos_entrenados_horizontal

    print(">>> Entrando a reiniciar_juego() debido a colisión.")
    menu_activo = True
    # MODIFICACIÓN: Personaje inicia en el centro horizontal al reiniciar
    jugador.x, jugador.y = w // 2 - jugador.width // 2, h - 100
    bala.x = w - 50
    nave.x, nave.y = w - 100, h - 150 # Ajustar la posición Y de la nave al reiniciar
    bala_disparada = False
    salto = False
    en_suelo = True
    
    # Reiniciar la segunda bala (Bala vertical siempre apunta al centro del jugador)
    # Su posición X solo se establece al inicio o al reiniciar.
    bala2.x = jugador.x + jugador.width // 2 - bala_vertical_img.get_width() // 2 # Usar bala_vertical_img.get_width()
    bala2.y = -bala_vertical_img.get_height() # Usar bala_vertical_img.get_height()
    bala2_activa = True
    
    modelo_elegido = None
    
    # Estas líneas permanecen comentadas/eliminadas para NO resetear las banderas de entrenamiento
    # modelos_entrenados = {1: False, 2: False, 3: False}
    # modelos_entrenados_horizontal = {1: False, 2: False, 3: False}
    
    # Solo se resetean las instancias de los modelos (a None)
    modelo = None
    modelo_horizontal = None

    print("Juego reiniciado debido a colisión. Volviendo al menú.")
    print(f"Se conservan {len(datos_modelo)} registros para Salto y {len(datos_modelo_horizontal)} para Movimiento Horizontal.")
    
    mostrar_menu()
    print(">>> Saliendo de reiniciar_juego().")


# Función para entrenar un modelo genérico (usado para salto y horizontal)
def entrenar_modelo_generico(id_modelo_a_entrenar, dataset, target_model_var, trained_status_dict):
    global modelo, modelo_horizontal
    
    min_data_needed = 10
    if len(dataset) < min_data_needed:
        print(f"No hay suficientes datos para entrenar el modelo de {target_model_var}. Se necesitan al menos {min_data_needed} registros, hay {len(dataset)}.")
        return False

    print(f"⏳ Entrenando modelo de {target_model_var} con {len(dataset)} registros...")
    
    X = np.array([dato[:2] for dato in dataset])
    y = np.array([dato[2] for dato in dataset])

    current_model_instance = None 
    if id_modelo_a_entrenar == 1:
        print(f"🏡 Usando Vecinos Cercanos (K-Nearest Neighbors) para {target_model_var}...")
        current_model_instance = KNeighborsClassifier(n_neighbors=6) 
    elif id_modelo_a_entrenar == 2:
        print(f"🌳 Usando Árbol de Decisión para {target_model_var}...")
        current_model_instance = DecisionTreeClassifier(random_state=0)
    elif id_modelo_a_entrenar == 3:
        print(f"🧠🦾 Usando Red Neuronal para {target_model_var}...")
        current_model_instance = MLPClassifier(random_state=0, max_iter=500, hidden_layer_sizes=(50,), early_stopping=True, n_iter_no_change=10)
    else:
        print(f"Modelo ID {id_modelo_a_entrenar} no válido para {target_model_var}.")
        return False

    try:
        current_model_instance.fit(X, y)
        if target_model_var == "salto":
            modelo = current_model_instance
        elif target_model_var == "horizontal":
            modelo_horizontal = current_model_instance
        
        # print(f"Modelo de {target_model_var} entrenado exitosamente.") # Este print se ha movido al main para control de impresión única
        trained_status_dict[id_modelo_a_entrenar] = True
        return True
    except ValueError as e:
        print(f"Error durante el entrenamiento del modelo de {target_model_var}: {e}")
        trained_status_dict[id_modelo_a_entrenar] = False
        return False


# Función para que la IA decida si saltar
def decidir_salto():
    global jugador, bala, modelo, salto, en_suelo, velocidad_bala
    if modelo is None:
        return

    distancia = abs(jugador.x - bala.x)
    entrada_modelo = np.array([[abs(velocidad_bala), distancia]])

    try:
        prediccion = modelo.predict(entrada_modelo)
        debe_saltar = prediccion[0] == 1

        if debe_saltar and en_suelo:
            salto = True
            en_suelo = False
            print("🤖 DEBUG IA: Salto iniciado.") # NUEVO: Impresión de salto IA
    except Exception as e:
        print(f"Error en IA al predecir salto: {e}")

# --- FUNCIÓN PARA QUE LA IA DECIDA EL MOVIMIENTO HORIZONTAL (NUEVO) ---
def decidir_movimiento_horizontal():
    global jugador, bala, modelo_horizontal, w
    if modelo_horizontal is None:
        return

    distancia_horizontal = abs(jugador.x - bala.x)
    entrada_modelo_horizontal = np.array([[abs(velocidad_bala), distancia_horizontal]])

    try:
        prediccion_horizontal = modelo_horizontal.predict(entrada_modelo_horizontal)
        accion_horizontal = prediccion_horizontal[0] # 0: Izquierda, 1: No moverse, 2: Derecha

        if accion_horizontal == 0: # Mover a la izquierda
            jugador.x -= 5 
            print("🤖 DEBUG IA: Movimiento Izquierda.") # NUEVO: Impresión de movimiento IA
        elif accion_horizontal == 2: # Mover a la derecha
            jugador.x += 5 
            print("🤖 DEBUG IA: Movimiento Derecha.") # NUEVO: Impresión de movimiento IA

        # Limitar el movimiento del jugador a los bordes de la pantalla
        # MODIFICACIÓN: Aplicar los mismos límites a la IA
        jugador.x = max(30, jugador.x) # Límite izquierdo a 30 píxeles
        jugador.x = min(w - 60 - jugador.width, jugador.x) # Límite derecho a 60 píxeles del borde
    
    except Exception as e:
        print(f"Error en IA al predecir movimiento horizontal: {e}")


# Inicializar los modelos (inicialmente None)
modelo = None
modelo_horizontal = None


def main():
    global salto, en_suelo, bala_disparada, modo_auto, modelo_elegido, datos_modelo, modelos_entrenados, modelo, pausa, menu_activo, datos_modelo_horizontal, modelo_horizontal, modelos_entrenados_horizontal, print_once_salto_trained, print_once_horizontal_trained

    print(">>> Iniciando función main().")
    reloj = pygame.time.Clock()
    if menu_activo:
        mostrar_menu()

    correr = True
    en_suelo = True
    tiempo_transcurrido_entrenamiento_salto = 0
    tiempo_transcurrido_entrenamiento_horizontal = 0
    
    # Velocidad de auto-centrado del personaje
    velocidad_auto_centro = 2

    while correr:
        keys = pygame.key.get_pressed()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                print("Saliendo del juego (Evento QUIT en bucle principal).")
                print("Datos de entrenamiento finales (Salto):", datos_modelo)
                print("Datos de entrenamiento finales (Mov. Horizontal):", datos_modelo_horizontal)
                correr = False
            if evento.type == pygame.KEYDOWN:
                if not menu_activo:
                    if evento.key == pygame.K_SPACE and en_suelo and not pausa and not modo_auto:
                        salto = True
                        en_suelo = False
                        print("👩 DEBUG: Salto manual iniciado.")
                    
                    if evento.key == pygame.K_p:
                        pausa_juego()
                        print("DEBUG: Tecla P presionada.")
                    
                    if evento.key == pygame.K_t and not modo_auto and not pausa:
                        print("DEBUG: Tecla T presionada (entrenamiento manual).")
                        if modelo_elegido is not None:
                            print(f"Intentando entrenar manualmente los modelos tipo: {modelo_elegido} con los datos actuales.")
                            entrenar_modelo_generico(modelo_elegido, datos_modelo, "salto", modelos_entrenados)
                            entrenar_modelo_generico(modelo_elegido, datos_modelo_horizontal, "horizontal", modelos_entrenados_horizontal)
                        else:
                            print("No se ha seleccionado un tipo de modelo para entrenar manualmente. Regrese al menú (escape) y elija uno, luego vuelva al modo manual si desea.")
                    if evento.key == pygame.K_ESCAPE:
                        print("DEBUG: Tecla ESC presionada. Volviendo al menú principal...")
                        pausa = False
                        menu_activo = True
                        mostrar_menu()

                if evento.key == pygame.K_q:
                    print("Saliendo del juego (Tecla Q en bucle principal).")
                    pygame.quit()
                    exit()

        if menu_activo:
            if not pygame.display.get_active() or pantalla.get_locked():
                    mostrar_menu()
            pygame.time.delay(50)
            continue

        if not pausa:
            if not modo_auto:
                if keys[pygame.K_LEFT]:
                    jugador.x -= 5
                    print("👩 DEBUG: Movimiento manual Izquierda iniciado.") # Movido para evitar spam
                elif keys[pygame.K_RIGHT]:
                    jugador.x += 5
                    print("👩 DEBUG: Movimiento manual Derecha iniciado.") # Movido para evitar spam
                else:
                    centro_pantalla_x = w // 2
                    centro_jugador_x = jugador.x + jugador.width // 2
                    
                    if abs(centro_jugador_x - centro_pantalla_x) > velocidad_auto_centro:
                        if centro_jugador_x < centro_pantalla_x:
                            jugador.x += velocidad_auto_centro
                        elif centro_jugador_x > centro_pantalla_x:
                            jugador.x -= velocidad_auto_centro
                    else:
                        jugador.x = centro_pantalla_x - jugador.width // 2
                        
                jugador.x = max(30, jugador.x)
                jugador.x = min(w - 60 - jugador.width, jugador.x)


            if not modo_auto:
                if salto:
                    manejar_salto()
                guardar_datos(keys)
                
            elif modo_auto:
                if modelo_elegido is not None:
                    # Lógica para el entrenamiento y decisión del modelo de SALTO
                    if not modelos_entrenados.get(modelo_elegido, False):
                        tiempo_transcurrido_entrenamiento_salto += reloj.get_time()
                        if tiempo_transcurrido_entrenamiento_salto > 2000:
                            print(f"🤖⏳ Modo automático: Iniciando entrenamiento del modelo de SALTO ({modelo_elegido}) con {len(datos_modelo)} registros.")
                            if entrenar_modelo_generico(modelo_elegido, datos_modelo, "salto", modelos_entrenados):
                                print(f"✅ Modelo de SALTO ({modelo_elegido}) ahora está entrenado y listo.")
                                print_once_salto_trained[modelo_elegido] = True
                            else:
                                print(f"⚠ Intento de entrenamiento para modelo de SALTO ({modelo_elegido}) fallido. Revise datos o espere más.")
                            tiempo_transcurrido_entrenamiento_salto = 0
                    else:
                        if not print_once_salto_trained[modelo_elegido]:
                            print(f"Modelo de SALTO ({modelo_elegido}) ya ha sido entrenado con {len(datos_modelo)} datos y se está utilizando.")
                            print_once_salto_trained[modelo_elegido] = True
                        
                        if modelo is None:
                             print(f"⏳✅ Entrenamiento ya realizado, cargando entrenamiento del modelo de SALTO ({modelo_elegido}).⌛")
                             entrenar_modelo_generico(modelo_elegido, datos_modelo, "salto", modelos_entrenados)
                    
                    if modelos_entrenados.get(modelo_elegido, False) and modelo is not None:
                        decidir_salto()
                        if salto:
                            manejar_salto()
                    elif modelo is None and modelos_entrenados.get(modelo_elegido, False):
                        print(f"Advertencia: Modelo de SALTO ({modelo_elegido}) marcado como entrenado, pero la instancia global 'modelo' es None. Intentando re-entrenar para cargar la instancia.")
                        entrenar_modelo_generico(modelo_elegido, datos_modelo, "salto", modelos_entrenados)


                    # Lógica para el entrenamiento y decisión del modelo de MOVIMIENTO HORIZONTAL
                    if not modelos_entrenados_horizontal.get(modelo_elegido, False):
                        tiempo_transcurrido_entrenamiento_horizontal += reloj.get_time()
                        if tiempo_transcurrido_entrenamiento_horizontal > 2000:
                            print(f"🤖⏳ Modo automático: Iniciando entrenamiento del modelo de MOVIMIENTO HORIZONTAL ({modelo_elegido}) con {len(datos_modelo_horizontal)} registros.")
                            if entrenar_modelo_generico(modelo_elegido, datos_modelo_horizontal, "horizontal", modelos_entrenados_horizontal):
                                print(f"✅ Modelo de MOVIMIENTO HORIZONTAL ({modelo_elegido}) ahora está entrenado y listo.")
                                print_once_horizontal_trained[modelo_elegido] = True
                            else:
                                print(f"⚠ Intento de entrenamiento para modelo de MOVIMIENTO HORIZONTAL ({modelo_elegido}) fallido. Revise datos o espere más.")
                            tiempo_transcurrido_entrenamiento_horizontal = 0
                    else:
                        if not print_once_horizontal_trained[modelo_elegido]:
                            print(f"Modelo de MOVIMIENTO HORIZONTAL ({modelo_elegido}) ya ha sido entrenado con {len(datos_modelo_horizontal)} datos y se está utilizando.")
                            print_once_horizontal_trained[modelo_elegido] = True

                        if modelo_horizontal is None:
                             print(f"⏳✅ Entrenamiento ya realizado, cargando entrenamiento del modelo de MOVIMIENTO HORIZONTAL ({modelo_elegido}). ⌛")
                             entrenar_modelo_generico(modelo_elegido, datos_modelo_horizontal, "horizontal", modelos_entrenados_horizontal)
                    
                    if modelos_entrenados_horizontal.get(modelo_elegido, False) and modelo_horizontal is not None:
                        decidir_movimiento_horizontal()
                    elif modelo_horizontal is None and modelos_entrenados_horizontal.get(modelo_elegido, False):
                        print(f"Advertencia: Modelo de MOVIMIENTO HORIZONTAL ({modelo_elegido}) marcado como entrenado, pero la instancia global 'modelo_horizontal' es None. Intentando re-entrenar para cargar la instancia.")
                        entrenar_modelo_generico(modelo_elegido, datos_modelo_horizontal, "horizontal", modelos_entrenados_horizontal)


                else:
                    print("Error en modo automático: Ningún modelo seleccionado. Volviendo al menú.")
                    modo_auto = False
                    menu_activo = True
                    reiniciar_juego()

            if not bala_disparada:
                disparar_bala()
            update()

        # Mostrar información en pantalla
        info_text_parts = []
        current_mode_str = "Manual" if not modo_auto else f"Auto (Modelo: {modelo_elegido or 'Ninguno'})"
        info_text_parts.append(f"Modo: {current_mode_str}")
        
        trained_display_str_salto = []
        for i in range(1,4):
            if modelos_entrenados[i]:
                if i == 1: trained_display_str_salto.append("KV")
                elif i == 2: trained_display_str_salto.append("AD")
                elif i == 3: trained_display_str_salto.append("RN")
        info_text_parts.append(f"Entre_S: {', '.join(trained_display_str_salto) or 'None'}")

        trained_display_str_horizontal = []
        for i in range(1,4):
            if modelos_entrenados_horizontal[i]:
                if i == 1: trained_display_str_horizontal.append("KV")
                elif i == 2: trained_display_str_horizontal.append("AD")
                elif i == 3: trained_display_str_horizontal.append("RN")
        info_text_parts.append(f"Entre_MH: {', '.join(trained_display_str_horizontal) or 'None'}")

        info_text_parts.append(f"D_S: {len(datos_modelo)} | D_H: {len(datos_modelo_horizontal)}")


        final_info_text = " | ".join(info_text_parts)
        if pausa:
            final_info_text = "PAUSADO | " + final_info_text
        
        texto_renderizado = fuente.render(final_info_text, True, BLANCO, NEGRO)
        pantalla.blit(texto_renderizado, (10, 10))

        pygame.display.flip()
        reloj.tick(30)

    print(">>> Saliendo de la función main().")
    print("Cerrando Pygame.")
    pygame.quit()

if __name__ == "__main__":
    main()

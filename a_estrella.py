import tkinter as tk #para crear la inetrfaz de usuario
from tkinter import simpledialog, messagebox, font
import heapq # Implementa el algoritmo de cola de prioridad (heap),

class AEstrellaVisualizador:
    def __init__(self, ventana_raiz):
        self.raiz = ventana_raiz #ventana principal de tkinter.
        self.raiz.title("Algoritmo A* - Ruta Mas Corta")

        self.num_filas = 0
        self.num_columnas = 0
        self.celdas_cuadricula = {} #almacenar los IDs de los elementos gráficos (rectángulo, textos g(costo), h(Heuristica), f(Costo F))
        #Un diccionario en Python es una colección de pares clave: valor. Es muy útil para almacenar y recuperar datos cuando tienes una forma única de identificar cada pieza de información (la clave).

        #Almacenan las coordenadas (fila, columna) de los nodos de inicio y fin.
        self.nodo_inicio = None
        self.nodo_fin = None
        self.obstaculos = set() #almacenar las coordenadas de las celdas que son obstáculos.
        #Un conjunto en Python es una colección de elementos únicos y desordenados. Esto significa que no puede haber elementos duplicados en un conjunto.

        self.tamano_celda = 50 #tamaño de cada una de la celdas
        self.fuente_numero_celda = font.Font(family="Arial", size=10, weight="bold")
        self.fuente_valores_ghf = font.Font(family="Arial", size=9)
        self.fuente_etiqueta_estado = font.Font(family="Arial", size=10)

        self.color_texto_ghf = "black"
        self.color_obstaculo = "gray60"
        self.color_camino = "palegreen" 
        self.color_inicio = "green"
        self.color_fin = "red"
        self.color_fondo_celda = "white"
        self.color_borde_celda = "grey"
        self.color_celda_explorada = "lightblue" # Color de Lista Cerrada
        self.color_celda_conjunto_abierto = "lightyellow" # Color Lista Abierta (cambiado de palegreen para distinguirlo del camino)

        self.crear_entrada_dimensiones() 

    def crear_entrada_dimensiones(self): 
        if hasattr(self, 'ventana_dimensiones_actual') and self.ventana_dimensiones_actual.winfo_exists(): #si la ventana existe y es visible
            self.ventana_dimensiones_actual.destroy() #La ventana se cierra y se destruye

        # Ventana que pide las dimesiones 
        self.ventana_dimensiones_actual = tk.Toplevel(self.raiz) #creacion de una nueva ventana hija que depende de la principal self.raiz
        self.ventana_dimensiones_actual.title("Ingrese Tamaño de la Matriz")
        self.ventana_dimensiones_actual.transient(self.raiz)
        self.ventana_dimensiones_actual.grab_set() #Se convierte en una ventana modal
        self.raiz.eval(f'tk::PlaceWindow {str(self.ventana_dimensiones_actual)} center') #centrar ventana emergente respecto a su ventana principal

        #Creación de Elementos de Entrada (Labels y Entries/Interfaz de la ventana de dimesiones)
        frame_entradas = tk.Frame(self.ventana_dimensiones_actual) #crear marco dentro de la ventana de dmesiomnes
        frame_entradas.pack(padx=10, pady=10) #padx es relleno horizontal, pady es relleno vertical

        tk.Label(frame_entradas, text="Número de Filas (N):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entrada_filas = tk.Entry(frame_entradas, width=10) #el usuario ingresa numero de filas
        self.entrada_filas.grid(row=0, column=1, padx=5, pady=5)
        self.entrada_filas.focus_set()

        tk.Label(frame_entradas, text="Número de Columnas (M):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entrada_columnas = tk.Entry(frame_entradas, width=10) #el usuario ingresa numero de columnas
        self.entrada_columnas.grid(row=1, column=1, padx=5, pady=5)

        def al_presionar_enter_filas(evento):
            self.entrada_columnas.focus_set() # Mover foco a columnas

        def al_presionar_enter_columnas(evento):
            self.obtener_dimensiones_cuadricula(self.entrada_filas.get(), self.entrada_columnas.get(), self.ventana_dimensiones_actual) #se obtienen las dimesiones de la cuadricula ya que ya se han ingresado estos datos

        self.entrada_filas.bind("<Return>", al_presionar_enter_filas) #se asocia un evento de presionar enter(return) con la funcion
        self.entrada_columnas.bind("<Return>", al_presionar_enter_columnas) ##se asocia un evento de presionar enter(return) con la funcion
        
        #El lambda asegura que la llamada al método con sus argumentos se retrase hasta el momento del clic.
        tk.Button(self.ventana_dimensiones_actual, text="OK", command=lambda: self.obtener_dimensiones_cuadricula(self.entrada_filas.get(), self.entrada_columnas.get(), self.ventana_dimensiones_actual)).pack(padx=10, pady=10)

    def obtener_dimensiones_cuadricula(self, filas_str, columnas_str, ventana): 
        try:
            #Conversion y validacion de entradas
            num_f = int(filas_str)
            num_c = int(columnas_str)

            # si num_f (filas) está entre 2 y 30 (inclusive) Y si num_c (columnas) está entre 2 y 40 (inclusive).
            if not (2 <= num_f <= 30 and 2 <= num_c <= 40): # Rangos ajustados
                messagebox.showerror("Error", "Filas deben estar entre 2-30 y Columnas entre 2-40.", parent=ventana)
                return
            
            #Comprueba si la ventana emergente (ventana dimensiones) todavia existe en la pantalla
            if ventana.winfo_exists():
                ventana.destroy()

            #Se actualizan los atributos num_filas y num_columnas del objeto self con los valores numéricos validados. Ahora el objeto tiene el tamaño de la nueva cuadrícula.
            self.num_filas = num_f
            self.num_columnas = num_c
            
            #Por si el usuario está creando una nueva matriz después de haber usado una anterior.
            for widget in self.raiz.winfo_children(): #lista todos los compoennetes garficos de la ventana princpal
                widget.destroy() 

            #Se reincian los valores inciales asedurando que la nueva cuadrícula comienza completamente limpia.
            self.celdas_cuadricula = {} 
            self.nodo_inicio = None
            self.nodo_fin = None
            self.obstaculos = set()
            
            #y una vez que las dimensiones son válidas y la interfaz/estado anterior ha sido limpiada, se llama al método
            self.configurar_interfaz_principal()
            
        except ValueError:
            messagebox.showerror("Error", "Entrada inválida. Ingrese números enteros para filas y columnas.", parent=ventana)
        except tk.TclError: 
            pass

    #construir la pantalla principal de tu aplicación A* una vez que ya se tienen las dimensiones de la cuadrícula. 
    def configurar_interfaz_principal(self):
        # Este marco se crea dentro de la ventana principal de la aplicación (self.raiz)
        frame_principal = tk.Frame(self.raiz)
        frame_principal.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Calcula el ancho ideal del lienzo (el área donde se dibujará la cuadrícula).
        ancho_lienzo = self.num_columnas * self.tamano_celda
        # Calcula el alto ideal del lienzo 
        alto_lienzo = self.num_filas * self.tamano_celda
        
        max_ancho_pantalla = self.raiz.winfo_screenwidth() - 100 #Obtiene el ancho total en píxeles de la pantalla del usuario.
        max_alto_pantalla = self.raiz.winfo_screenheight() - 200 #Obtiene el alto total de la pantalla.
        
        #Si la cuadrícula es muy grande, se "recortará" al tamaño máximo permitido por la pantalla.
        ancho_lienzo_final = min(ancho_lienzo, max_ancho_pantalla) #min(...): Esta función devuelve el valor más pequeño entre los dos que se le pasan.
        alto_lienzo_final = min(alto_lienzo, max_alto_pantalla)

        #Crea el widget Canvas (lienzo). Este es el componente donde se dibujarán las celdas de la cuadrícula, los números, los colores del camino, etc.
        self.lienzo = tk.Canvas(frame_principal, width=ancho_lienzo_final, height=alto_lienzo_final,
                                borderwidth=1, relief="solid", bg="lightgray")
        self.lienzo.pack(pady=10, padx=10, expand=True, anchor="center")

        self.crear_cuadricula_widgets()

        #contenedor de los botones de control. Se crea dentro del frame_principal.
        frame_botones = tk.Frame(frame_principal)
        frame_botones.pack(pady=5)

        #Cuando se haga clic en este botón, se ejecutará el método encontrar_camino (que contiene la lógica del algoritmo A*).
        #Se habilitará cuando el usuario haya seleccionado un nodo de inicio y un nodo de fin.
        self.boton_encontrar_camino = tk.Button(frame_botones, text="Encontrar Camino", command=self.encontrar_camino, state=tk.DISABLED)
        self.boton_encontrar_camino.pack(side=tk.LEFT, padx=5)

        #Al hacer clic, llama al método para borrar las selecciones de inicio, fin y obstáculos.
        boton_limpiar_seleccion = tk.Button(frame_botones, text="Limpiar Selección", command=self.limpiar_seleccion_actual)
        boton_limpiar_seleccion.pack(side=tk.LEFT, padx=5)
        
        #Al hacer clic, vuelve a llamar al método que pide al usuario nuevas dimensiones, permitiendo crear una cuadrícula diferente.
        boton_nueva_matriz = tk.Button(frame_botones, text="Nuevas Dimensiones", command=self.crear_entrada_dimensiones) # CAMBIO
        boton_nueva_matriz.pack(side=tk.LEFT, padx=5)

        self.etiqueta_estado = tk.Label(frame_principal, text="Seleccione el nodo de inicio.", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=self.fuente_etiqueta_estado, wraplength=ancho_lienzo_final)
        self.etiqueta_estado.pack(fill=tk.X, padx=10, pady=(5,0))
        
        #fuerza a Tkinter a procesar todas las tareas pendientes de dibujo y cálculo de tamaño de los widgets que se acaban de crear
        self.raiz.update_idletasks() 
        #Este comando se usa para establecer la posición y/o el tamaño de una ventana (establecer la posición)
        self.raiz.geometry(f'+{ (self.raiz.winfo_screenwidth() - self.raiz.winfo_width()) // 2 }+{ (self.raiz.winfo_screenheight() - self.raiz.winfo_height()) // 2 }')

    #restablecer el estado de la cuadrícula a su punto inicial
    def limpiar_seleccion_actual(self):
        #Comprueba si las dimensiones de la cuadrícula (self.num_filas y self.num_columnas) son válidas (mayores que cero).
        if self.num_filas <= 0 or self.num_columnas <= 0: 
            return

        self.nodo_inicio = None
        self.nodo_fin = None
        self.obstaculos.clear()
        
        for r_idx in range(self.num_filas):
            for c_idx in range(self.num_columnas):
                #r_idx es el índice de la fila y c_idx es índice de la columna.
                #Crea una tupla con las coordenadas de la celda actual que se está procesando.
                nodo_limpieza = (r_idx, c_idx)
                if nodo_limpieza in self.celdas_cuadricula:
                    #Modifica una propiedad de un ítem en el lienzo.
                    self.lienzo.itemconfig(self.celdas_cuadricula[nodo_limpieza][0], fill=self.color_fondo_celda) #devuelve la tupla de IDs de los elementos gráficos de esa celda ((id_rectangulo, id_g_texto, id_h_texto, id_f_texto))
                    #cambiar los textos de los valores G, H y F de la celda actual a "?".
                    self.actualizar_valores_celda(nodo_limpieza, "?", "?", "?", update_ui=False)
        
        #Deshabilta el boton ya que ya no hay nodo fin ni nodo inicio
        if hasattr(self, 'boton_encontrar_camino') and self.boton_encontrar_camino:
            self.boton_encontrar_camino.config(state=tk.DISABLED)
        #Cambia el texto de la etiqueta de estado para informar al usuario que la selección ha sido limpiada 
        if hasattr(self, 'etiqueta_estado') and self.etiqueta_estado:
            self.etiqueta_estado.config(text="Selección limpiada. Seleccione el nodo de inicio.")
        
        #fuerza a Tkinter a procesar todas las tareas pendientes de dibujo y cálculo de tamaño de los widgets que se acaban de crear
        self.raiz.update_idletasks()

    #dibujar la cuadrícula visualmente en el lienzo (Canvas)
    def crear_cuadricula_widgets(self):
        #borra absolutamente todo lo que estuviera dibujado previamente en el lienzo (self.lienzo)
        self.lienzo.delete("all")

        for i in range(self.num_filas):
            for j in range(self.num_columnas):
                #calcula un número único para mostrar en la esquina de la celda (ID DE CELDA)
                numero_celda_display = i * self.num_columnas + j + 1
                x1 = j * self.tamano_celda #Calcula la coordenada X de la esquina superior izquierda del rectángulo de la celda actual. 
                y1 = i * self.tamano_celda #Calcula la coordenada Y de la esquina superior izquierda
                x2 = x1 + self.tamano_celda #Calcula la coordenada X de la esquina inferior derecha del rectángulo.
                y2 = y1 + self.tamano_celda #Calcula la coordenada Y de la esquina inferior derecha.

                # Dibuja un rectángulo en el lienzo usando las coordenadas x1, y1, x2, y2 calculadas.
                id_rectangulo = self.lienzo.create_rectangle(x1, y1, x2, y2, fill=self.color_fondo_celda, outline=self.color_borde_celda, tags=(f"celda_rect-{i}-{j}", f"fila-{i}", f"col-{j}"))
                
                padding = 5
                #Dibuja texto en el lienzo para mostrar el numero_celda_display
                id_texto_numero = self.lienzo.create_text(x1 + padding, y1 + padding, text=str(numero_celda_display), anchor="nw", font=self.fuente_numero_celda, tags=(f"texto_num-{i}-{j}", f"fila-{i}", f"col-{j}"))
                #Posicionamiento de los Textos G, H, F
                centro_x_celda = (x1 + x2) / 2
                y_centro_celda = (y1+y2) / 2
                espaciado_vertical_ghf = self.fuente_valores_ghf.actual('size') + 4
                y_g = y_centro_celda ; y_h = y_g + espaciado_vertical_ghf ; y_f = y_h + espaciado_vertical_ghf
                max_y = y2 - padding
                y_f = min(y_f, max_y)
                y_h = min(y_h, y_f - espaciado_vertical_ghf if y_f - espaciado_vertical_ghf > y1 + padding else y_f)
                y_g = min(y_g, y_h - espaciado_vertical_ghf if y_h - espaciado_vertical_ghf > y1 + padding else y_h)
                #Creación de los Textos G, H, F
                id_g_texto = self.lienzo.create_text(centro_x_celda, y_g, text="g=?", font=self.fuente_valores_ghf, fill=self.color_texto_ghf, tags=(f"g_texto-{i}-{j}", f"fila-{i}", f"col-{j}"))
                id_h_texto = self.lienzo.create_text(centro_x_celda, y_h, text="h=?", font=self.fuente_valores_ghf, fill=self.color_texto_ghf, tags=(f"h_texto-{i}-{j}", f"fila-{i}", f"col-{j}"))
                id_f_texto = self.lienzo.create_text(centro_x_celda, y_f, text="f=?", font=self.fuente_valores_ghf, fill=self.color_texto_ghf, tags=(f"f_texto-{i}-{j}", f"fila-{i}", f"col-{j}"))
                
                #Se guarda una tupla con los cuatro IDs de los elementos gráficos de la celda (i,j) (el rectángulo, y los textos g, h, f) en el diccionario self.celdas_cuadricula
                #La clave del diccionario es la tupla de coordenadas (i,j)
                #El valor es la tupla de IDs
                #permite acceder y modificar fácilmente cualquier parte de cualquier celda más tarde, usando sus coordenadas.
                self.celdas_cuadricula[(i, j)] = (id_rectangulo, id_g_texto, id_h_texto, id_f_texto)
                #Se crea una lista que contiene los IDs de todos los elementos visuales de la celda actual
                elementos_bind = [id_rectangulo, id_texto_numero, id_g_texto, id_h_texto, id_f_texto]

                #tag_bind(): Este método de Tkinter asocia un evento a un tag o a un ID de un ítem del lienzo.
                #"<Button-1>": Es la cadena que representa el evento de hacer clic con el botón izquierdo del mouse.
                for elem_id in elementos_bind:
                    self.lienzo.tag_bind(elem_id, "<Button-1>", lambda e, r=i, c=j: self.al_hacer_click_celda(r,c))

    #controlador de eventos para cuando el usuario hace clic en cualquier celda de la cuadrícula.
    def al_hacer_click_celda(self, fila, columna):
        #Crea una tupla que representa las coordenadas de la celda en la que se hizo clic
        nodo_actual = (fila, columna)
        #Calcula el número de celda
        numero_celda_display = fila * self.num_columnas + columna + 1

        #No se ha seleccionado un nodo de inicio
        if self.nodo_inicio is None:
            self.nodo_inicio = nodo_actual
            self.lienzo.itemconfig(self.celdas_cuadricula[nodo_actual][0], fill=self.color_inicio)
            #Actualiza la etiqueta de estado para informar al usuario que ha seleccionado el inicio y que ahora debe seleccionar el nodo final
            self.etiqueta_estado.config(text=f"Inicio: celda {numero_celda_display} ({fila+1},{columna+1}). Seleccione fin.")
        #Ya se seleccionó un inicio, pero no un fin
        elif self.nodo_fin is None:
            if nodo_actual == self.nodo_inicio:
                messagebox.showwarning("Advertencia", "Fin no puede ser igual a inicio.", parent=self.raiz)
                return
            self.nodo_fin = nodo_actual
            self.lienzo.itemconfig(self.celdas_cuadricula[nodo_actual][0], fill=self.color_fin)
            self.etiqueta_estado.config(text=f"Fin: celda {numero_celda_display} ({fila+1},{columna+1}). Marque obstáculos o 'Encontrar Camino'.")
            #se habilita el boton encontrar camino
            if hasattr(self, 'boton_encontrar_camino') and self.boton_encontrar_camino:
                self.boton_encontrar_camino.config(state=tk.NORMAL)
        #Ya se seleccionaron tanto el inicio como el fin
        else:
            if nodo_actual == self.nodo_inicio: 
                self.lienzo.itemconfig(self.celdas_cuadricula[self.nodo_inicio][0], fill=self.color_fondo_celda)
                self.actualizar_valores_celda(self.nodo_inicio, "?", "?", "?", update_ui=False)
                self.nodo_inicio = None
                self.etiqueta_estado.config(text="Inicio deseleccionado. Seleccione nodo de inicio.")
                if hasattr(self, 'boton_encontrar_camino') and self.boton_encontrar_camino: self.boton_encontrar_camino.config(state=tk.DISABLED)
            elif nodo_actual == self.nodo_fin: 
                self.lienzo.itemconfig(self.celdas_cuadricula[self.nodo_fin][0], fill=self.color_fondo_celda)
                self.actualizar_valores_celda(self.nodo_fin, "?", "?", "?", update_ui=False)
                self.nodo_fin = None
                self.etiqueta_estado.config(text="Fin deseleccionado. Seleccione nodo de fin.")
                if hasattr(self, 'boton_encontrar_camino') and self.boton_encontrar_camino: self.boton_encontrar_camino.config(state=tk.DISABLED)
            elif nodo_actual in self.obstaculos: 
                self.obstaculos.remove(nodo_actual)
                self.lienzo.itemconfig(self.celdas_cuadricula[nodo_actual][0], fill=self.color_fondo_celda)
                self.etiqueta_estado.config(text=f"Obstáculo en celda {numero_celda_display} eliminado.")
            else: 
                self.obstaculos.add(nodo_actual)
                self.lienzo.itemconfig(self.celdas_cuadricula[nodo_actual][0], fill=self.color_obstaculo)
                self.etiqueta_estado.config(text=f"Obstáculo añadido en celda {numero_celda_display}.")
        self.raiz.update_idletasks()

    def calcular_heuristica(self, a, b):
        #a:representa las coordenadas del primer nodo
        #b: representa las coordenadas del segundo nodo
        #Manhatan
        return (abs(a[0] - b[0]) + abs(a[1] - b[1])) * 10

    #encuentra todos los nodos adyacentes válidos a un nodo dado. 
    #Un vecino es válido si está dentro de la cuadrícula y no es un obstáculo.
    def obtener_vecinos(self, nodo):
        #nodo: Una tupla (fila, columna) del nodo para el cual queremos encontrar los vecinos
        vecinos = [] #lista para vecinos validos
        fila, columna = nodo
        #define los 8 posibles "desplazamientos" o "vectores de movimiento" desde una celda a sus celdas adyacentes.
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in movimientos:
            #Se calculan las coordenadas del posible vecino sumando el desplazamiento actual (dr, dc) a las coordenadas del nodo original (fila, columna).
            nueva_fila, nueva_columna = fila + dr, columna + dc
            #valida a un vecino si: 
            if 0 <= nueva_fila < self.num_filas and \
               0 <= nueva_columna < self.num_columnas and \
               (nueva_fila, nueva_columna) not in self.obstaculos:
                #a tupla de coordenadas del vecino válido se añade a la lista vecinos.
                vecinos.append((nueva_fila, nueva_columna))
        return vecinos # devuelve la lista vecinos

    #Determina el costo (G) de moverse desde un nodo a a un nodo adyacente b.
    def obtener_costo(self, a, b):
        #a: Una tupla (fila, columna) representando el nodo de partida.
        #b: Una tupla (fila, columna) representando el nodo de llegada   
        #diagonales
        if abs(a[0] - b[0]) == 1 and abs(a[1] - b[1]) == 1: return 14 #retorna 14 porque fue un diagonal
        #horizontales y verticales
        return 10 #si no fue un movimiento diagonal se retorna un 10 de horizontal/vertical

    #método principal que implementa el algoritmo A*
    def encontrar_camino(self):
        #comprueba si el usuario ha seleccionado tanto un nodo_inicio como un nodo_fin.
        if self.nodo_inicio is None or self.nodo_fin is None:
            messagebox.showerror("Error", "Seleccione nodos de inicio y fin.", parent=self.raiz)
            return

        #Limpiar cualquier rastro visual (colores, valores G, H, F) de una ejecución anterior del algoritmo A*, para que la nueva búsqueda
        for r_idx in range(self.num_filas):
            for c_idx in range(self.num_columnas):
                nodo_limpieza = (r_idx, c_idx)
                if nodo_limpieza != self.nodo_inicio and nodo_limpieza != self.nodo_fin and nodo_limpieza not in self.obstaculos:
                    if nodo_limpieza in self.celdas_cuadricula:
                        self.lienzo.itemconfig(self.celdas_cuadricula[nodo_limpieza][0], fill=self.color_fondo_celda)
                if nodo_limpieza != self.nodo_inicio : 
                    self.actualizar_valores_celda(nodo_limpieza, "?", "?", "?", update_ui=False)

        inicio, fin = self.nodo_inicio, self.nodo_fin #Asigna los nodos de inicio y fin seleccionados por el usuario a variables locales para facilitar su uso.
        conjunto_abierto = [] #Lista que contendrá los nodos que han sido descubiertos pero aún no evaluados.
        h_inicio = self.calcular_heuristica(inicio, fin) #Calcula el valor H (heurística) desde el nodo inicio hasta el nodo fin.
        heapq.heappush(conjunto_abierto, (h_inicio, h_inicio, inicio)) #Añade el nodo de inicio al conjunto_abierto

        #Un diccionario vacío. Se usará para reconstruir el camino al final. Almacenará pares nodo_actual: nodo_predecesor_en_el_mejor_camino.
        camino_desde = {}
        #Un diccionario para almacenar el costo G (el costo real desde el nodo inicio hasta cualquier otro nodo (r,c)).
        puntaje_g = { (r,c): float('inf') for r in range(self.num_filas) for c in range(self.num_columnas) }
        #El costo G para llegar al nodo inicio desde sí mismo es 0.
        puntaje_g[inicio] = 0
        
        #Muestra los valores G, H y F iniciales para el nodo de inicio en la interfaz gráfica.
        self.actualizar_valores_celda(inicio, 0, h_inicio, h_inicio)
        #Asegura que esta actualización inicial de la GUI se muestre antes de que comience el bucle principal del algoritmo.
        self.raiz.update_idletasks()

        #El algoritmo continúa ejecutándose mientras haya nodos en el conjunto_abierto (es decir, mientras haya nodos descubiertos que aún no se han evaluado por completo).
        while conjunto_abierto:
            f_actual, _, actual = heapq.heappop(conjunto_abierto)
            if actual == fin:
                self.reconstruir_camino(camino_desde, actual)
                return
            if actual != inicio and actual != fin : 
                self.lienzo.itemconfig(self.celdas_cuadricula[actual][0], fill=self.color_celda_explorada)
                #self.raiz.update_idletasks(); self.raiz.after(500)
                self.raiz.update_idletasks(); self.raiz.after(10)
            for vecino in self.obtener_vecinos(actual):
                costo_movimiento = self.obtener_costo(actual, vecino)
                puntaje_g_tentativo = puntaje_g[actual] + costo_movimiento
                if puntaje_g_tentativo < puntaje_g[vecino]:
                    camino_desde[vecino] = actual
                    puntaje_g[vecino] = puntaje_g_tentativo
                    heuristica_vecino = self.calcular_heuristica(vecino, fin)
                    f_score_vecino = puntaje_g_tentativo + heuristica_vecino
                    heapq.heappush(conjunto_abierto, (f_score_vecino, heuristica_vecino, vecino))
                    self.actualizar_valores_celda(vecino, puntaje_g[vecino], heuristica_vecino, f_score_vecino)
                    if vecino != fin and vecino != inicio:
                        self.lienzo.itemconfig(self.celdas_cuadricula[vecino][0], fill=self.color_celda_conjunto_abierto)
                        #self.raiz.update_idletasks(); self.raiz.after(500)
                        self.raiz.update_idletasks(); self.raiz.after(5)
        #Si el bucle while conjunto_abierto: termina (lo que significa que conjunto_abierto se quedó vacío) y el nodo_fin nunca fue alcanzado, significa que no existe un camino válido
        self.etiqueta_estado.config(text="No se encontró un camino.")
        messagebox.showinfo("Info", "No se encontró un camino.", parent=self.raiz)

    #Este método es una utilidad para actualizar los textos de los valores G, H y F que se muestran dentro de una celda específica
    def actualizar_valores_celda(self, nodo, g, h, f, update_ui=True):
        if nodo not in self.celdas_cuadricula: return
        if len(self.celdas_cuadricula[nodo]) < 4: return 
        _, id_g_texto, id_h_texto, id_f_texto = self.celdas_cuadricula[nodo]
        self.lienzo.itemconfig(id_g_texto, text=f"g={g}")
        self.lienzo.itemconfig(id_h_texto, text=f"h={h}")
        self.lienzo.itemconfig(id_f_texto, text=f"f={f}")
        if update_ui: self.raiz.update_idletasks()

    #Este método se llama después de que el algoritmo A* ha encontrado el nodo final.
    def reconstruir_camino(self, camino_desde, actual):
        camino_total_coords = [actual]
        while actual in camino_desde:
            actual = camino_desde[actual]
            camino_total_coords.append(actual)
        camino_total_coords.reverse()

        camino_numeros_celda = []
        camino_texto_display = "Camino (celdas): "
        for i, nodo_coord in enumerate(camino_total_coords):
            numero_celda = nodo_coord[0] * self.num_columnas + nodo_coord[1] + 1
            camino_numeros_celda.append(numero_celda)
            camino_texto_display += str(numero_celda)
            if i < len(camino_total_coords) - 1:
                camino_texto_display += " -> "
                camino_texto_display += " <- "
        
        print("Camino encontrado (coordenadas):", camino_total_coords)
        print("Camino encontrado (números de celda):", camino_numeros_celda)
        
        if hasattr(self, 'etiqueta_estado') and self.etiqueta_estado:
            self.etiqueta_estado.config(text=camino_texto_display)
        else: 
            messagebox.showinfo("Camino Encontrado", camino_texto_display, parent=self.raiz)

        self.colorear_camino_visual(camino_total_coords)


    #cambiar el color de las celdas que forman parte del camino encontrado
    def colorear_camino_visual(self, camino_coords):
        for i, nodo in enumerate(camino_coords):
            if nodo != self.nodo_inicio and nodo != self.nodo_fin:
                if nodo in self.celdas_cuadricula:
                    self.lienzo.itemconfig(self.celdas_cuadricula[nodo][0], fill=self.color_camino)
            if i < len(camino_coords) - 1: 
                self.raiz.update_idletasks(); self.raiz.after(70)
        
        if self.nodo_inicio and self.nodo_inicio in self.celdas_cuadricula:
             self.lienzo.itemconfig(self.celdas_cuadricula[self.nodo_inicio][0], fill=self.color_inicio)
        if self.nodo_fin and self.nodo_fin in self.celdas_cuadricula:
             self.lienzo.itemconfig(self.celdas_cuadricula[self.nodo_fin][0], fill=self.color_fin)


if __name__ == "__main__":
    #Crea la ventana principal (o "raíz") de tu aplicación.
    raiz = tk.Tk()
    #Crea una instancia
    app = AEstrellaVisualizador(raiz)
    #Inicia el bucle de eventos principal de Tkinter.
    raiz.mainloop()
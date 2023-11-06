import sys
import pygame
import math

TAMAÑO_PANTALLA = (640, 480)
# Tamaño de la pantalla en píxeles: ancho x alto

TAMAÑO_CELDA = 32
# Tamaño de una celda del laberinto en píxeles

CELDA_POR_DEFECTO = 0b0000000000000000
# Valor por defecto para una celda del laberinto (sin muros ni retroceso ni solución)

BITS_MURO = 0b0000000000001111
# Máscara de bits para identificar los muros alrededor de una celda

BITS_RETROCESO = 0b1111000000000000
# Máscara de bits para identificar la información de retroceso en una celda

BITS_SOLUCION = 0b0000111100000000
# Máscara de bits para identificar la información de solución en una celda

MUROS = [0b1000, 0b0100, 0b0010, 0b0001]
# Lista de valores binarios que representan la presencia de muros en cada uno de los 4 puntos cardinales (oeste, sur, este, norte)

MUROS_OPUESTOS = [0b0010, 0b0001, 0b1000, 0b0100]
# Lista de valores binarios que representan la presencia de muros opuestos a los muros en cada punto cardinal

PUNTOS_CARDINALES = [(-1, 0), (0, 1), (1, 0), (0, -1)]
# Lista de tuplas que representan los desplazamientos en los puntos cardinales (oeste, sur, este, norte)

DIRECCIONES = ['O', 'S', 'E', 'N']
# Lista de letras que representan las direcciones de los puntos cardinales (oeste, sur, este, norte)


# Colores
NEGRO = (0, 0, 0, 255)
SIN_COLOR = (0, 0, 0, 0)
BLANCO = (255, 255, 255, 255)
VERDE = (0, 255, 0, 255)
ROJO = (255, 0, 0, 255)
AZUL = (0, 0, 255, 255)
AZUL_CLARO = (0, 0, 255, 100)
MORADO = (150, 0, 150, 255)

class Laberinto:
    def __init__(self, estado_inicial='inactivo'):
        # Configuración del laberinto
        self.estado = estado_inicial
        self.celdas_ancho = int(TAMAÑO_PANTALLA[0] / TAMAÑO_CELDA)
        self.celdas_alto = int(TAMAÑO_PANTALLA[1] / TAMAÑO_CELDA)
        self.celdas_totales = self.celdas_ancho * self.celdas_alto
        self.arreglo_laberinto = [CELDA_POR_DEFECTO] * self.celdas_totales
        
        # Configuración de pygame
        pygame.init()
        self.pantalla = pygame.display.set_mode(TAMAÑO_PANTALLA)
        self.fondo = pygame.Surface(self.pantalla.get_size())
        self.capa_muro = pygame.Surface(self.pantalla.get_size())
        self.capa_solucion = pygame.Surface(self.pantalla.get_size())
        self.configurar_ventana_laberinto()
        
    # Devuelve las celdas vecinas dentro de los límites del laberinto
    # Utiliza self.estado para determinar qué vecinos deben incluirse
    def celdas_vecinas(self, celda):
        x, y = self.x_y(celda)
        vecinos = []
        for i in range(4):
        # Calcula las coordenadas del nuevo punto considerando el punto cardinal actual
            nuevo_x = x + PUNTOS_CARDINALES[i][0]
            nuevo_y = y + PUNTOS_CARDINALES[i][1]

            # Verifica si el nuevo punto está dentro de los límites del laberinto

            if (self.celda_en_limites(nuevo_x, nuevo_y)):

                # Calcula el índice de la nueva celda en función de sus coordenadas
                nueva_celda = self.indice_celda(nuevo_x, nuevo_y)
                if(self.estado == 'crear'):
                # Si se está creando el laberinto, verifica si no hay un muro entre la celda actual y la vecina
                    if not(self.arreglo_laberinto[nueva_celda] & BITS_MURO):
                # Agrega la tupla (índice de celda vecina, índice de punto cardinal) a la lista de vecinos
                        vecinos.append((nueva_celda, i))
                elif(self.estado == 'resolver'):
                     # Si se está resolviendo el laberinto, verifica si hay un muro entre la celda actual y la vecina,
                # y si la vecina no está marcada como parte de la solución o del retroceso.
                    if(self.arreglo_laberinto[celda] & MUROS[i]):
                        if not(self.arreglo_laberinto[nueva_celda] &
                                (BITS_RETROCESO | BITS_SOLUCION)):
                            vecinos.append((nueva_celda, i))# Agrega la tupla (índice de celda vecina, índice de punto cardinal) a la lista de vecinos
        return vecinos
    
    # Conecta dos celdas derribando el muro entre ellas
    # Actualiza los bits de muro de la celda de origen y la celda de destino
    def conectar_celdas(self, celda_origen, celda_destino, indice_puntos_cardinales):
        self.arreglo_laberinto[celda_origen] |=  MUROS[indice_puntos_cardinales]
        self.arreglo_laberinto[celda_destino] |=  MUROS_OPUESTOS[indice_puntos_cardinales]
        self.dibujar_conectar_celdas(celda_origen, indice_puntos_cardinales)
     
    # Visita una celda a lo largo de un posible camino de solución
    # Actualiza los bits de solución de la celda de origen y los bits de retroceso de la celda de destino
    def visitar_celda(self, celda_origen, celda_destino, indice_puntos_cardinales):
        self.arreglo_laberinto[celda_origen] &= ~BITS_SOLUCION
        self.arreglo_laberinto[celda_origen] |= (MUROS[indice_puntos_cardinales] << 8)
        self.arreglo_laberinto[celda_destino] |= (MUROS_OPUESTOS[indice_puntos_cardinales] << 12)
        # Lógica para actualizar los bits de celda
        self.dibujar_celda_visitada(celda_origen)
                
    def retroceder(self, celda):
        self.arreglo_laberinto[celda] &= ~BITS_SOLUCION
        # Lógica para actualizar los bits de celda
        self.dibujar_celda_retrocedida(celda)

    # Visita una celda en la búsqueda BFS
    # Actualiza los bits de retroceso para usar en la reconstrucción de la solución
    def visitar_celda_bfs(self, celda, desde_indice_puntos_cardinales):
        self.arreglo_laberinto[celda] |= (MUROS_OPUESTOS[desde_indice_puntos_cardinales] << 12)
        self.dibujar_celda_visitada_bfs(celda)

    # Reconstruir el camino hacia el inicio usando los bits de retroceso
    def reconstruir_solucion(self, celda):
        # Lógica para reconstruir el camino de solución en BFS

        self.dibujar_celda_visitada(celda)  # Marcar la celda como visitada en la visualización del laberinto
        # Se obtiene la información de retroceso al aplicar una operación "Y" a nivel de bits
        # con la constante BITS_RETROCESO y luego se realiza un desplazamiento de bits hacia la derecha
        # para aislar los bits relevantes que representan el retroceso en la celda actual.
        bits_celda_anterior = (self.arreglo_laberinto[celda] & BITS_RETROCESO) >> 12
        try:
            i = MUROS.index(bits_celda_anterior)
        except ValueError:
            print('ERROR - BITS DE RETROCESO INVÁLIDOS!')
        x, y = self.x_y(celda)
        x_anterior = x + PUNTOS_CARDINALES[i][0]
        y_anterior = y + PUNTOS_CARDINALES[i][1]
        celda_anterior = self.indice_celda(x_anterior, y_anterior)
        self.arreglo_laberinto[celda_anterior] |= (MUROS_OPUESTOS[i] << 8)
        self.refrescar_vista_laberinto()  # Actualizar la visualización del laberinto
        if celda_anterior != 0: 
            self.reconstruir_solucion(celda_anterior)  # Llamada recursiva para seguir reconstruyendo el camino hacia el inicio

    # Comprobar si los valores x, y de la celda están dentro de los límites del laberinto
    def celda_en_limites(self, x, y):
        return ((x >= 0) and (y >= 0) and (x < self.celdas_ancho)
                and (y < self.celdas_alto))

    # Índice de la celda a partir de los valores x, y
    def indice_celda(self, x, y):
        return y * self.celdas_ancho + x
    
    def visitar_celda_a_estrella(self, celda, desde_indice_puntos_cardinales, celda_objetivo):
        self.arreglo_laberinto[celda] |= (MUROS_OPUESTOS[desde_indice_puntos_cardinales] << 12)  # Establece los bits de retroceso en la celda
        self.arreglo_laberinto[celda] |= (self.calcular_distancia(celda, celda_objetivo) << 16) # Calcula y establece el costo en la celda
        self.dibujar_celda_visitada_a_estrella(celda) # Dibuja la celda visitada en el camino
    
    def dibujar_celda_visitada_a_estrella(self, celda):
        x_pos, y_pos = self.x_y_pos(celda)
        pygame.draw.rect(self.capa_solucion, AZUL_CLARO, pygame.Rect(x_pos, y_pos, TAMAÑO_CELDA, TAMAÑO_CELDA))

   # Reconstruir el camino usando los bits de retroceso en el algoritmo A*
    def reconstruir_solucion_a_estrella(self, celda, celda_objetivo):
        self.dibujar_celda_visitada(celda) # Dibuja la celda visitada en el camino 
        bits_celda_anterior = (self.arreglo_laberinto[celda] & BITS_RETROCESO) >> 12 # Obtiene los bits de retroceso
        try:
            i = MUROS.index(bits_celda_anterior)   # Busca el índice de los bits de retroceso en la lista de MUROS
        except ValueError:
            print('ERROR - BITS DE RETROCESO INVÁLIDOS!')
        x, y = self.x_y(celda) # Obtiene las coordenadas (x, y) de la celda actual
        x_anterior = x + PUNTOS_CARDINALES[i][0] # Calcula la coordenada x de la celda anterior
        y_anterior = y + PUNTOS_CARDINALES[i][1] # Calcula la coordenada y de la celda anterior
        celda_anterior = self.indice_celda(x_anterior, y_anterior)  # Obtiene el índice de la celda anterior
        self.arreglo_laberinto[celda_anterior] |= (MUROS_OPUESTOS[i] << 8)  # Establece los bits de los muros opuestos en la celda anterior
        self.refrescar_vista_laberinto()
        if celda_anterior != celda_objetivo:
            self.reconstruir_solucion_a_estrella(celda_anterior, celda_objetivo)  # Llama recursivamente a la función para reconstruir el camino

    # Calcular la distancia euclidiana entre dos celdas para la heurística A*
    def calcular_distancia(self, celda_actual, celda_objetivo):
        # Calcula la distancia euclidiana entre dos celdas para ser utilizada en la heurística A*
        x_actual, y_actual = self.x_y(celda_actual)   # Obtiene las coordenadas (x, y) de la celda actual
        x_objetivo, y_objetivo = self.x_y(celda_objetivo)  # Obtiene las coordenadas (x, y) de la celda objetivo
        return int(math.sqrt((x_actual - x_objetivo) ** 2 + (y_actual - y_objetivo) ** 2)) # Calcula la distancia euclidiana

    # Valores x, y a partir de un índice de celda
    def x_y(self, indice):
        # Calcula las coordenadas (x, y) a partir de un índice de celda
        x = indice % self.celdas_ancho # Calcula la coordenada x en función del ancho del laberinto
        y = int(indice / self.celdas_ancho) # Calcula la coordenada y dividiendo el índice por el ancho del laberinto
        return x, y # Devuelve las coordenadas (x, y) de la celda

    # Valores x, y de un punto a partir de un índice de celda
    def x_y_pos(self, indice):
    # Convierte un índice de celda en las coordenadas (x, y) en la pantalla
        x, y = self.x_y(indice) # Obtiene las coordenadas (x, y) de la celda
        x_pos = x * TAMAÑO_CELDA # Calcula la posición x en la pantalla
        y_pos = y * TAMAÑO_CELDA # Calcula la posición y en la pantalla
        return x_pos, y_pos      # Devuelve las coordenadas (x, y) en la pantalla

    # 'Tumbar' un muro entre dos celdas, úsalo en la creación a medida que se eliminan muros
    def dibujar_conectar_celdas(self, celda_origen, indice_puntos_cardinales):
        x_pos, y_pos = self.x_y_pos(celda_origen)  # Obtiene las coordenadas (posición) de la celda en la pantalla

        # Dibuja una línea para 'tumbar' un muro entre celdas, según el índice de puntos cardinales
        if indice_puntos_cardinales == 0:
            pygame.draw.line(self.capa_muro, SIN_COLOR, (x_pos, y_pos + 1),
                             (x_pos, y_pos + TAMAÑO_CELDA - 1)) # Si el índice es 0 (oeste)
        elif indice_puntos_cardinales == 1:# Si el índice es 1 (sur)
            pygame.draw.line(self.capa_muro, SIN_COLOR, (x_pos + 1,
                             y_pos + TAMAÑO_CELDA), (x_pos + TAMAÑO_CELDA - 1,
                             y_pos + TAMAÑO_CELDA))  
        elif indice_puntos_cardinales == 2:  # Si el índice es 2 (este)
            pygame.draw.line(self.capa_muro, SIN_COLOR, (x_pos + TAMAÑO_CELDA,
                             y_pos + 1), (x_pos + TAMAÑO_CELDA,
                             y_pos + TAMAÑO_CELDA - 1))
        elif indice_puntos_cardinales == 3:         # Si el índice es 3 (norte)
            pygame.draw.line(self.capa_muro, SIN_COLOR, (x_pos + 1, y_pos),
                             (x_pos + TAMAÑO_CELDA - 1, y_pos))

    # Dibuja un cuadrado verde en la celda, úsalo para visualizar el camino de solución mientras se explora
    def dibujar_celda_visitada(self, celda):
        x_pos, y_pos = self.x_y_pos(celda) # obtiene las coordenadas
        pygame.draw.rect(self.capa_solucion, VERDE, pygame.Rect(x_pos, y_pos,
                         TAMAÑO_CELDA, TAMAÑO_CELDA)) #dibuja un cuadrado verde en la celda

    # Dibuja un cuadrado rojo en la celda, es para cambiar la celda y visualizar el retroceso
    def dibujar_celda_retrocedida(self, celda):
        x_pos, y_pos = self.x_y_pos(celda) # Obtiene las coordenadas (posicion), igual que en la funcion siguiente 
        pygame.draw.rect(self.capa_solucion, ROJO, pygame.Rect(x_pos, y_pos,
                         TAMAÑO_CELDA, TAMAÑO_CELDA))  # Dibuja un cuadrado rojo en la celda

    # Dibuja un cuadrado verde en la celda, es para visualizar el camino de solución mientras se explora en BFS
    def dibujar_celda_visitada_bfs(self, celda):
        x_pos, y_pos = self.x_y_pos(celda) # Obtiene las coordenadas (posición) de la celda en la pantalla
        pygame.draw.rect(self.capa_solucion, AZUL_CLARO, pygame.Rect(x_pos, y_pos,
                         TAMAÑO_CELDA, TAMAÑO_CELDA)) # Dibuja un cuadrado azul claro en la celda

    # Procesa eventos, agrega cada capa a la pantalla y refresca
    # Se llama al final de cada paso de recorrido para observar el laberinto mientras se genera
    def refrescar_vista_laberinto(self):
        # Llama a la función para comprobar eventos de salida

        comprobar_salida()
        # Agrega capas a la pantalla

        self.pantalla.blit(self.fondo, (0, 0)) # Agrega la capa de fondo en la posición (0, 0)
        self.pantalla.blit(self.capa_solucion, (0, 0)) # Agrega la capa de solucion en la posición (0, 0)
        self.pantalla.blit(self.capa_muro, (0, 0)) # Agrega la capa de muros en la posición (0, 0)
        pygame.display.flip()

    def configurar_ventana_laberinto(self):
        # Configurar ventana y capas
        pygame.display.set_caption('Generación y Resolución de Laberintos') # Establece el título de la ventana
        pygame.mouse.set_visible(0) # Oculta el cursor del mouse
        self.fondo = self.fondo.convert() # Capa de fondo, se convierte para mejorar el rendimiento
        self.fondo.fill(BLANCO) # Rellena el fondo con color blanco
        self.capa_muro = self.capa_muro.convert_alpha() # Capa de muros, se convierte para permitir transparencia
        self.capa_muro.fill(SIN_COLOR)  # Rellena la capa de muros con transparencia
        self.capa_solucion = self.capa_solucion.convert_alpha()  # Capa de solución, se convierte para permitir transparencia
        self.capa_solucion.fill(SIN_COLOR) # Rellena la capa de solución con transparencia

        # Dibujar líneas de la cuadrícula (serán blanqueadas a medida que se derriban los muros)
        for y in range(self.celdas_alto + 1):
            pygame.draw.line(self.capa_muro, NEGRO, (0, y * TAMAÑO_CELDA),
                             (TAMAÑO_PANTALLA[0], y * TAMAÑO_CELDA))  # Dibuja líneas horizontales
        for x in range(self.celdas_ancho + 1):
            pygame.draw.line(self.capa_muro, NEGRO, (x * TAMAÑO_CELDA, 0), 
                             (x * TAMAÑO_CELDA, TAMAÑO_PANTALLA[1])) # Dibuja líneas verticales

        # Colorear la celda de inicio en azul y la celda de salida en púrpura.
        # Supone que el inicio está en la esquina superior izquierda y la salida en la esquina inferior derecha.
        pygame.draw.rect(self.capa_solucion, AZUL,
                         pygame.Rect(0, 0, TAMAÑO_CELDA, TAMAÑO_CELDA))  # Dibuja un cuadrado azul para la celda de inicio
        pygame.draw.rect(self.capa_solucion, MORADO, pygame.Rect(
                         TAMAÑO_PANTALLA[0] - TAMAÑO_CELDA, TAMAÑO_PANTALLA[1] -
                         TAMAÑO_CELDA, TAMAÑO_CELDA, TAMAÑO_CELDA))  # Dibuja un cuadrado morado para la celda de salida


# Función para comprobar eventos de salida
def comprobar_salida():
    # Crear un objeto reloj para controlar la velocidad de la ejecución (60 fps)
    reloj = pygame.time.Clock()
    reloj.tick(60)  # Limita la velocidad a 60 fotogramas por segundo

    # Iterar a través de todos los eventos en la cola de eventos de pygame
    for evento in pygame.event.get():
        # Verificar si el tipo de evento es 'pygame.QUIT' (cerrar la ventana)
        if evento.type == pygame.QUIT:
            sys.exit(0)  # Salir del programa si se cierra la ventana
        # Verificar si se presiona una tecla
        elif evento.type == pygame.KEYDOWN:
            # Verificar si la tecla presionada es 'pygame.K_ESCAPE' (tecla Esc)
            if evento.key == pygame.K_ESCAPE:
                sys.exit(0)  # Salir del programa si se presiona la tecla Esc

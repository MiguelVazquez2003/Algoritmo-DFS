import pygame
import random

# Tamaño de la ventana y celdas del laberinto
ANCHO_VENTANA = 600
ALTO_VENTANA = 600
TAMANO_CELDA = 10

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Inicialización de Pygame
pygame.init()
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Laberinto Aleatorio con DFS")

# Clase para representar una celda
class Celda:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.visitada = False
        self.paredes = [True, True, True, True]  # Arriba, Derecha, Abajo, Izquierda

    def dibujar(self):
        x = self.columna * TAMANO_CELDA
        y = self.fila * TAMANO_CELDA
        if self.paredes[0]:
            pygame.draw.line(ventana, NEGRO, (x, y), (x + TAMANO_CELDA, y), 2)
        if self.paredes[1]:
            pygame.draw.line(ventana, NEGRO, (x + TAMANO_CELDA, y), (x + TAMANO_CELDA, y + TAMANO_CELDA), 2)
        if self.paredes[2]:
            pygame.draw.line(ventana, NEGRO, (x, y + TAMANO_CELDA), (x + TAMANO_CELDA, y + TAMANO_CELDA), 2)
        if self.paredes[3]:
            pygame.draw.line(ventana, NEGRO, (x, y), (x, y + TAMANO_CELDA), 2)

    def resaltar(self):
        x = self.columna * TAMANO_CELDA
        y = self.fila * TAMANO_CELDA
        pygame.draw.rect(ventana, (0, 0, 255, 100), (x, y, TAMANO_CELDA, TAMANO_CELDA))

# Función para obtener celdas vecinas no visitadas
def obtener_vecinos_no_visitados(grid, celda):
    vecinos = []
    direcciones = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Arriba, Derecha, Abajo, Izquierda
    for direccion in direcciones:
        fila = celda.fila + direccion[0]
        columna = celda.columna + direccion[1]
        if 0 <= fila < len(grid) and 0 <= columna < len(grid[0]) and not grid[fila][columna].visitada:
            vecinos.append((fila, columna))
    return vecinos

# Algoritmo DFS para generar el laberinto
def generar_laberinto_dfs(grid, celda_actual):
    celda_actual.visitada = True
    pila = [celda_actual]

    while pila:
        celda_actual = pila[-1]
        vecinos = obtener_vecinos_no_visitados(grid, celda_actual)

        if vecinos:
            siguiente_fila, siguiente_columna = random.choice(vecinos)
            celda_siguiente = grid[siguiente_fila][siguiente_columna]
            celda_siguiente.visitada = True

            if siguiente_fila < celda_actual.fila:
                celda_actual.paredes[0] = False
                celda_siguiente.paredes[2] = False
            elif siguiente_columna > celda_actual.columna:
                celda_actual.paredes[1] = False
                celda_siguiente.paredes[3] = False
            elif siguiente_fila > celda_actual.fila:
                celda_actual.paredes[2] = False
                celda_siguiente.paredes[0] = False
            else:
                celda_actual.paredes[3] = False
                celda_siguiente.paredes[1] = False

            pila.append(celda_siguiente)
        else:
            pila.pop()

# Creación de la cuadrícula de celdas
num_filas = ALTO_VENTANA // TAMANO_CELDA
num_columnas = ANCHO_VENTANA // TAMANO_CELDA
grid = [[Celda(fila, columna) for columna in range(num_columnas)] for fila in range(num_filas)]

# Celda de inicio y generación del laberinto
celda_inicial = grid[0][0]
generar_laberinto_dfs(grid, celda_inicial)

# Bucle principal de Pygame
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    ventana.fill(BLANCO)

    for fila in grid:
        for celda in fila:
            celda.dibujar()

    pygame.display.flip()

pygame.quit()

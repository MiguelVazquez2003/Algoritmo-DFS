import laberinto
import random  # Importa el módulo random para generar números aleatorios

# Función para crear un laberinto utilizando el algoritmo de creación de laberinto Pre-Orden DFS
def crear_dfs(m):
    retroceso = []  # Inicializa una lista para realizar retrocesos durante la creación del laberinto
    celda_aleatoria = random.randint(1, m.celdas_totales - 1)  # Elige una celda aleatoria como punto de partida
    visitadas = [0] * m.celdas_totales  # Inicializa una lista de celdas visitadas
    visitadas[celda_aleatoria] = 1  # Marca la celda aleatoria como visitada

    while (visitadas.count(1) < m.celdas_totales):  # Mientras no todas las celdas estén visitadas
        celdas_vecinas = m.celdas_vecinas(celda_aleatoria)  # Obtiene las celdas vecinas de la celda actual

        if (len(celdas_vecinas) >= 1):  # Si hay celdas vecinas sin visitar
            vecino_aleatorio = celdas_vecinas[random.randint(0, len(celdas_vecinas) - 1)]  # Elige un vecino aleatorio
            m.conectar_celdas(celda_aleatoria, vecino_aleatorio[0], vecino_aleatorio[1])  # Conecta la celda actual con el vecino
            retroceso.append(celda_aleatoria)  # Guarda la celda actual en la pila de retroceso
            celda_aleatoria = vecino_aleatorio[0]  # Se mueve a la celda vecina
            visitadas[celda_aleatoria] = 1  # Marca la celda vecina como visitada
        else:
            celda_aleatoria = retroceso.pop()  # Si no hay vecinos sin visitar, retrocede a la celda anterior

        m.refrescar_vista_laberinto()  # Refresca la vista del laberinto en cada paso

    m.estado = 'resolver'  # Cambia el estado del laberinto a "resolver" después de crearlo

# Función principal del programa
def main():
    laberinto_actual = laberinto.Laberinto('crear')  # Crea una instancia del laberinto en modo de creación
    crear_dfs(laberinto_actual)  # Llama a la función para crear el laberinto DFS
    while 1:
        laberinto.comprobar_salida()  # Comprueba si se desea salir del programa

if __name__ == '__main__':
    main()

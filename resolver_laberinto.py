import laberinto
import generar_laberinto
import sys
from collections import deque
import random

# Resolver el laberinto utilizando el algoritmo Pre-Orden DFS y terminar con la solución
def resolver_dfs(m):
    retroceso = []  # Inicializa una lista para realizar retrocesos durante la resolución del laberinto
    celda_actual = 0  # Inicializa la celda actual como la celda de inicio
    visitadas = 0  # Inicializa un contador de celdas visitadas

    while celda_actual != m.celdas_totales - 1:  # Mientras no se alcance la celda de salida
        vecinos = m.celdas_vecinas(celda_actual)  # Obtiene las celdas vecinas de la celda actual

        if vecinos:  # Si hay celdas vecinas sin visitar
            nueva_celda, comp = random.choice(vecinos)  # Elige una celda vecina aleatoria
            m.visitar_celda(celda_actual, nueva_celda, comp)  # Marca la celda actual y la vecina como visitadas
            retroceso.append(celda_actual)  # Guarda la celda actual en la pila de retroceso
            celda_actual = nueva_celda  # Se mueve a la celda vecina
            visitadas += 1  # Incrementa el contador de celdas visitadas
        else:
            m.retroceder(celda_actual)  # Si no hay celdas vecinas sin visitar, retrocede
            celda_actual = retroceso.pop()  # Retrocede a la celda anterior

        m.refrescar_vista_laberinto()  # Refresca la vista del laberinto en cada paso

    m.estado = 'inactivo'  # Cambia el estado del laberinto a "inactivo" después de resolverlo
    


# Resolver el laberinto utilizando el algoritmo BFS y terminar con la solución
def resolver_bfs(m):
    cola = deque()  # Inicializa una cola (FIFO) para rastrear las celdas por visitar
    celda_actual = 0  # Inicializa la celda actual como la celda de inicio
    en_direccion = 0b0000  # Inicializa la dirección de entrada a la celda actual
    celdas_visitadas = 0  # Inicializa un contador de celdas visitadas
    cola.append((celda_actual, en_direccion))  # Agrega la celda de inicio a la cola

    while celda_actual != m.celdas_totales - 1 and cola:  # Mientras no se alcance la celda de salida y haya elementos en la cola
        celda_actual, en_direccion = cola.popleft()  # Obtiene y elimina la celda de la cola
        m.visitar_celda_bfs(celda_actual, en_direccion)  # Marca la celda actual como visitada
        celdas_visitadas += 1  # Incrementa el contador de celdas visitadas
        m.refrescar_vista_laberinto()  # Refresca la vista del laberinto en cada paso

        vecinos = m.celdas_vecinas(celda_actual)  # Obtiene las celdas vecinas de la celda actual
        for vecino in vecinos:  # Para cada celda vecina
            cola.append(vecino)  # Agrega la celda vecina a la cola para su posterior exploración

    m.reconstruir_solucion(celda_actual)  # Reconstruye la solución del laberinto a partir de la última celda visitada
    m.estado = 'inactivo'  # Cambia el estado del laberinto a "inactivo" después de resolverlo


# Resolver el laberinto utilizando el algoritmo A* y terminar con la solución
def resolver_astar(m):
    cola = []  # Inicializa una cola de prioridad para rastrear las celdas por visitar
    celda_actual = 0  # Inicializa la celda actual como la celda de inicio
    celda_objetivo = m.celdas_totales - 1  # Define la celda objetivo (salida)
    celdas_visitadas = 0  # Inicializa un contador de celdas visitadas
    cola.append((celda_actual, 0, m.calcular_distancia(celda_actual, celda_objetivo)))  # Agrega la celda de inicio a la cola con su costo estimado

    while celda_actual != celda_objetivo and cola:  # Mientras no se alcance la celda de salida y haya elementos en la cola
        cola.sort(key=lambda x: x[2])  # Ordena la cola por costo total (A*) para explorar las celdas con menor costo primero
        celda_actual, en_direccion, _ = cola.pop(0)  # Obtiene y elimina la celda con menor costo de la cola
        m.visitar_celda_a_estrella(celda_actual, en_direccion, celda_objetivo)  # Marca la celda actual como visitada
        celdas_visitadas += 1  # Incrementa el contador de celdas visitadas
        m.refrescar_vista_laberinto()  # Refresca la vista del laberinto en cada paso

        vecinos = m.celdas_vecinas(celda_actual)  # Obtiene las celdas vecinas de la celda actual
        for vecino in vecinos:  # Para cada celda vecina
            siguiente_celda, direccion = vecino
            costo_total = celdas_visitadas + m.calcular_distancia(siguiente_celda, celda_objetivo)  # Calcula el costo total (A*)
            cola.append((siguiente_celda, direccion, costo_total))  # Agrega la celda vecina a la cola con su nuevo costo estimado

    m.reconstruir_solucion_a_estrella(celda_objetivo, celda_objetivo)  # Reconstruye la solución del laberinto A* desde la celda objetivo
    m.estado = 'inactivo'  # Cambia el estado del laberinto a "inactivo" después de resolverlo


#no lo mandamos a llamar en ningun momento, se puede cambiar esto
# Imprimir el arreglo de solución del laberinto
def imprimir_arreglo_solucion(m):
    solucion = m.arreglo_solucion()  # Obtiene el arreglo de solución del laberinto
    print('Solución ({} pasos): {}'.format(len(solución), solución))  # Imprime la solución, su longitud y el arreglo de solución en el formato especificado


def main(resolutor='astar'):
    laberinto_actual = laberinto.Laberinto('crear')
    generar_laberinto.crear_dfs(laberinto_actual)

    if resolutor == 'dfs':
        resolver_dfs(laberinto_actual)
    elif resolutor == 'bfs':
        resolver_bfs(laberinto_actual)
    elif resolutor == 'astar':
        resolver_astar(laberinto_actual)


    while 1:    
        laberinto.comprobar_salida()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()

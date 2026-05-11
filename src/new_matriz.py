# IMPORTANTE: Gran parte de este código utiliza conceptos vistos durante las clases de Álgebra Lineal
# y Fundamentos de Programación. El programa implementa una malla 2D sobre la que se aplican
# transformaciones lineales mediante matrices y operaciones vectoriales.
#
# La librería NumPy únicamente se utiliza para el cálculo numérico de autovalores y autovectores,
# tal y como permite el profesor en el enunciado de la práctica.

# Objetivos:
# 1º [Completado]: Representar una malla 2D mediante matrices cuadradas.
# 2º [Completado]: Implementar movimiento vectorial del personaje.
# 3º [Completado]: Implementar detección de colisiones y límites.
# 4º [Completado]: Implementar homomorfismos lineales:
#                   - Rotación 90º horaria.
#                   - Simetría vertical.
#                   - Simetría horizontal.
# 5º [Completado]: Implementar cambio de base entre índices y coordenadas cartesianas.
# 6º [Completado]: Calcular autovalores y autovectores.
# 7º [Completado]: Analizar subespacios invariantes reales.

# Guía para el profesor:
#
# - Representación y Visualización:
#   **crear_matriz, print_map**
#
# - Cambio de Base:
#   **to_vector, to_index**
#
# - Movimiento y Colisiones:
#   **move**
#
# - Homomorfismos:
#   **apply_matrix, update_map**
#
# - Transformaciones:
#   **M_rot, M_ysym, M_xsym**
#
# - Autovalores y Autovectores:
#   **numpy.linalg.eig**
#
# - Limpieza y Estructura:
#   Código modular mediante funciones independientes.

import numpy as np

# ============================================================
# DICCIONARIO VISUAL
# ============================================================
# Este diccionario transforma los números almacenados
# dentro de la matriz en símbolos visuales.
# 0 -> Aire
# 1 -> Muro
# 2 -> Jugador
# ============================================================
SYMBOLS = {
    0: " ",
    1: "□",
    2: "X"
}

# ============================================================
# CREACIÓN DE LA MATRIZ
# ============================================================
# Creamos una matriz cuadrada 5x5. El personaje comenzará situado en el centro.
# ============================================================
def crear_matriz():
    matriz = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 2, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ]
    return matriz

# ============================================================
# FUNCIÓN print_map
# ============================================================
# Esta función recorre toda la matriz y transforma los valores numéricos en símbolos visuales.
# ============================================================
def print_map(matriz):
    for fila in matriz:
        fila_visual = []
        for elemento in fila:
            fila_visual.append(SYMBOLS[elemento])
        print(" ".join(fila_visual))

# ============================================================
# VARIABLES GLOBALES
# ============================================================
# n -> tamaño de la matriz.
# c -> centro de la matriz.
# El centro será utilizado para realizar el cambio de base cartesiano.
# ============================================================
matriz = crear_matriz()
n = len(matriz)
c = (n - 1) // 2

# ============================================================
# CAMBIO DE BASE
# ============================================================
# En una matriz tradicional:(0,0) se encuentra arriba a la izquierda. Sin embargo, para trabajar algebraicamente, necesitamos un sistema cartesiano con fórmulas:
# x = j - c
# y = -(i - c)
# ============================================================
def to_vector(i, j):
    x = j - c
    y = -(i - c)
    return (x, y)

# ============================================================
# CAMBIO DE BASE INVERSO
# ============================================================
# Esta función transforma coordenadas cartesianas nuevamente en índices de matriz.
# Fórmulas:
# i = c - y
# j = c + x
# ============================================================
def to_index(x, y):
    i = c - y
    j = c + x
    return (i, j)

# ============================================================
# FUNCIÓN encontrar_personaje
# ============================================================
# Recorremos toda la matriz hasta encontrar la posición del jugador representado por el valor 2.
# ============================================================
def encontrar_personaje(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == 2:
                return (i, j)
    return None, None

# ============================================================
# POSICIÓN INICIAL DEL PERSONAJE
# ============================================================
i_inicio, j_inicio = encontrar_personaje(matriz)
player_pos = to_vector(i_inicio, j_inicio)

# ============================================================
# FUNCIÓN move
# ============================================================
# Esta función implementa movimiento vectorial. El desplazamiento se realiza mediante: (x1,y1) = (x0,y0) + d 
# donde: d = vector desplazamiento 
# También controla:
# - Límites del mapa.
# - Colisiones contra muros.
# ============================================================
def move(matriz, player_pos, d):
    x, y = player_pos
    dx, dy = d
    # Nueva posición tras la suma vectorial
    new_x = x + dx
    new_y = y + dy
    # Conversión de coordenadas a índices
    i_old, j_old = to_index(x, y)
    i_new, j_new = to_index(new_x, new_y)
    # Validación de límites
    if not (0 <= i_new < n and 0 <= j_new < n):
        print("\n¡Límite del mapa!")
        return player_pos

    # Validación de muros
    if matriz[i_new][j_new] == 1:
        print("\n¡Muro detectado!")
        return player_pos

    # Actualización de posiciones
    matriz[i_old][j_old] = 0
    matriz[i_new][j_new] = 2
    return (new_x, new_y)

# ============================================================
# MATRICES DE TRANSFORMACIÓN
# ============================================================
# Todas las transformaciones geométricas se aplican mediante multiplicación matricial.
# ============================================================

# ============================================================
# MATRIZ DE ROTACIÓN 90º HORARIA
# ============================================================
# e1 -> -e2
# e2 ->  e1
# ============================================================
M_rot = [
    [0, 1],
    [-1, 0]
]

# ============================================================
# MATRIZ DE SIMETRÍA VERTICAL
# ============================================================
# e1 -> -e1
# e2 ->  e2
# ============================================================
M_ysym = [
    [-1, 0],
    [0, 1]
]

# ============================================================
# MATRIZ DE SIMETRÍA HORIZONTAL
# ============================================================
# e1 ->  e1
# e2 -> -e2
# ============================================================
M_xsym = [
    [1, 0],
    [0, -1]
]

# ============================================================
# FUNCIÓN apply_matrix
# ============================================================
# Esta función realiza multiplicación matriz-vector.
# ============================================================
def apply_matrix(M, v):
    x, y = v
    new_x = M[0][0] * x + M[0][1] * y
    new_y = M[1][0] * x + M[1][1] * y
    return (new_x, new_y)

# ============================================================
# FUNCIÓN update_map
# ============================================================
# Esta función aplica una transformación lineal a todos los elementos de la malla.
# Flujo: Índice -> Vector -> Aplicar transformación -> Nuevo índice
# ============================================================
def update_map(matriz, M):
    nueva_matriz = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            valor = matriz[i][j]
            # Conversión índice -> vector
            x, y = to_vector(i, j)
            # Aplicar transformación lineal
            new_x, new_y = apply_matrix(M, (x, y))
            # Conversión vector -> índice
            new_i, new_j = to_index(new_x, new_y)
            nueva_matriz[new_i][new_j] = valor
    return nueva_matriz

# ============================================================
# MENÚ DE CONTROLES
# ============================================================
# Esta función muestra las acciones disponibles para interactuar con el mapa.
# ============================================================
def mostrar_menu():

    print("\n==============================")
    print("CONTROLES")
    print("==============================")
    print("W -> Arriba")
    print("S -> Abajo")
    print("A -> Izquierda")
    print("D -> Derecha")
    print("R -> Rotación 90º")
    print("V -> Simetría Vertical")
    print("H -> Simetría Horizontal")
    print("E -> Mostrar espectro")
    print("Q -> Salir")

# ============================================================
# ANÁLISIS DE TRANSFORMACIONES
# ============================================================
# Esta función calcula:
# - Autovalores.
# - Autovectores.
# - Interpretación geométrica.
# ============================================================
def analizar_transformacion(M, nombre):
    matriz_np = np.array(M)
    valores, vectores = np.linalg.eig(matriz_np)
    print("\n==============================")
    print(nombre)
    print("==============================")
    print("\nAutovalores:")
    print(valores)
    print("\nAutovectores:")
    print(vectores)

    if nombre == "ROTACIÓN 90º HORARIA":
        print("\nInterpretación:")
        print("La rotación posee autovalores complejos.")
        print("No existen subespacios invariantes reales.")

    elif nombre == "SIMETRÍA VERTICAL":
        print("\nInterpretación:")
        print("El eje y permanece invariante.")
        print("Los vectores sobre el eje y no cambian de dirección.")

    elif nombre == "SIMETRÍA HORIZONTAL":
        print("\nInterpretación:")
        print("El eje x permanece invariante.")
        print("Los vectores sobre el eje x no cambian de dirección.")

# ============================================================
# IMPRESIÓN DEL MAPA INICIAL
# ============================================================
print("\n==============================")
print("MAPA INICIAL")
print("==============================\n")
print_map(matriz)

# ============================================================
# BUCLE PRINCIPAL DEL PROGRAMA
# ============================================================
# El programa permanecerá ejecutándose hasta que el usuario introduzca la opción Q.
# ============================================================
while True:
    mostrar_menu()
    accion = input("\nSelecciona una acción: ").upper()
    # Salida del programa
    if accion == "Q":
        print("\nPrograma finalizado.")
        break

    # Movimiento hacia arriba
    elif accion == "W":
        player_pos = move(matriz, player_pos, (0, 1))

    # Movimiento hacia abajo
    elif accion == "S":
        player_pos = move(matriz, player_pos, (0, -1))

    # Movimiento hacia la izquierda
    elif accion == "A":
        player_pos = move(matriz, player_pos, (-1, 0))

    # Movimiento hacia la derecha
    elif accion == "D":
        player_pos = move(matriz, player_pos, (1, 0))

    # Aplicar rotación
    elif accion == "R":
        matriz = update_map(matriz, M_rot)
        i_inicio, j_inicio = encontrar_personaje(matriz)
        player_pos = to_vector(i_inicio, j_inicio)
        print("\nROTACIÓN APLICADA")

    # Aplicar simetría vertical
    elif accion == "V":
        matriz = update_map(matriz, M_ysym)
        i_inicio, j_inicio = encontrar_personaje(matriz)
        player_pos = to_vector(i_inicio, j_inicio)
        print("\nSIMETRÍA VERTICAL APLICADA")

    # Aplicar simetría horizontal
    elif accion == "H":
        matriz = update_map(matriz, M_xsym)
        i_inicio, j_inicio = encontrar_personaje(matriz)
        player_pos = to_vector(i_inicio, j_inicio)
        print("\nSIMETRÍA HORIZONTAL APLICADA")

    # Mostrar análisis matemático
    elif accion == "E":
        analizar_transformacion(M_rot, "ROTACIÓN 90º HORARIA")
        analizar_transformacion(M_ysym, "SIMETRÍA VERTICAL")
        analizar_transformacion(M_xsym, "SIMETRÍA HORIZONTAL")

    # Acción inválida
    else:
        print("\nAcción inválida.")

    print("\n==============================")
    print("ESTADO ACTUAL DEL MAPA")
    print("==============================\n")
    print_map(matriz)
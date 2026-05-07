# IMPORTANTE: Gran parte del código presente en este archivo pertence a nuestras clases de fundamentos de programación, es decir, parte del mismo
# es reciclado de clases anteriores. Aunque este sea el caso, el código cuenta con retoques propios y otras modificaciones, así como la 
# asistencia de Gemini para solucionar problemas menores como tabulación o conversión de json a formato txt. (Conversación en el Pdf)

# Objetivos: 
# 1º [Completado]: El número 1 representa las paredes del "Mapa/Matriz", el número 2 representa el personaje, mientras que el número 0 representa las "casillas vacías/caminos".
# 2º [Completado]: El usuario deberá ser capaz de desplazar el personaje por toda la matriz, siempre y cuando no haya una pared en el camino.

# Las únicas funciones que cuentan con jugador_v2 (encargada del movimiento del personaje), puesto que no habíamos dado en clase nada parecido
#  y cargar_matriz (encargada de cargar la matriz desde un archivo .txt) han sido asistidas por IA. Fuera de esto, la IA ha asistido en correción
# de errores, como tabulación y conversión de formatos, y mejoras en la expresión escrita (copilot).

# Guía para el profesor: 
# - Representación y Visualización: **crear_archivo, cargar_matriz, crear_filas, crear_columnas, rellenar_matriz, encontrar_personaje**.
# - Lógica de Movimiento Y colisiones: **jugar_v2**.
# - Homomorfismo: La función **jugar_v2** es un ejemplo de homomorfismo, ya que toma la matriz como entrada, realiza operaciones sobre ella (movimiento del personaje) 
#   y luego actualiza la matriz en el archivo. La función mantiene la estructura de la matriz mientras permite la interacción del usuario, 
#   lo que es una característica clave de un homomorfismo.
# - Limpieza y Estructura del Código: A su discrección.
# - Análisis de Autovalores y Subespacios Invariantes: No es aplicable en este caso, ya que el código no involucra operaciones complejas ni transformaciones lineales que requieran de dicho análisis.

import os 


def crear_archivo(file_path, matriz, mode='w'):
    # Creamos la carpeta si no existe
    os.makedirs(os.path.dirname(file_path), exist_ok=True) # Reescribimos el archivo para cada vez que vayamos a modificar la matriz, podríamos
    with open(file_path, mode, encoding="utf-8") as f:     # no hacer esto y simplemente ir añadiendo matrices pero el archivo se llenaría.
        for fila in matriz:
            # Convertimos cada número dentro de cada fila a string y los unimos con espacios, esta linea inferior es la más influenciada por IA.
            linea = " ".join(map(str, fila)) # map convierte lo que haya en el parametro de la izquierda a lo que haya al formato de la derecha
            f.write(linea + "\n") # Escribimos la fila y un salto de línea

# En caso de que el archivo ya existe y, por lo tanto, la matriz también entonces necesitaré una función para no sobreescribir el archivo.
# Como la matriz se encuentra dentro de un archivo .txt y no un json, debo crear una función para cargar la matriz con sus datos previos dentro de una lista si la matriz existía previamente.

def cargar_matriz(file_path):
    if not os.path.exists(file_path):
        return None

    matriz = []
    with open(file_path, 'r', encoding="utf-8") as f:
        for linea in f:
            fila = linea.strip().split(" ") # Eliminamos los espacios en blanco al principio y al final de la línea, y luego dividimos la línea en una lista de valores utilizando el espacio como separador.
            matriz.append(fila) # Añadimos la fila a la matriz
    return matriz

def crear_filas():
    while True:
        try:
            filas = int(input("¿Cuántas filas quieres (1-10)? "))
            if 1 <= filas <= 10: # Las filas no deberían tener valores negativos, no tendría sentido, y además tampoco queremos que la matriz sea
                return filas     # excesivamente grande, aunque podríamos modificar el código para que lo fuera.
            print("El número de filas debe estar entre 1 y 10.")
        except ValueError: # En caso de haber introducido valores negativos, saltará un ValueError con el mensaje de abajo.
            print("Debes introducir un número entero.")

def crear_columnas():
    while True:
        try:
            columnas = int(input("¿Cuántas columnas quieres (1-10)? ")) # Es exactamente el mismo caso que con las filas, solamente que con columnas.
            if 1 <= columnas <= 10:
                return columnas
            print("El número de columnas debe estar entre 1 y 10.")
        except ValueError:
            print("Debes introducir un número entero.")

# Las dos funciones anteriores no tienen mucho misterior, consiste en crear variables (filas, columnas) mediante un input para que tú les asignes el 
# valor correspondiente, asegurandonos de que dichos valores sean válidos mediante el uso de excepciones y ValueError.

def rellenar_matriz(filas, columnas):
    matriz = [] # Actualmente la matriz se encuentra vacía, no será hasta el final de esta función que la matriz se irá llenando con los valores introducidos por el usuario.
    print(f"\nIntroduce valores de 0 a 2 para una matriz de {filas}x{columnas}") 
    for f in range(filas):
        fila_actual = [] # Esta lista contendrá los valores de los números en cada fila.
        c = 0 # Esta variable se utiliza para aseguranos de que se introduzcan el número correctod de valores por cada fila.
        while c < columnas: # En este bucle es dónde creamos los valores dentro de la lista fila_actual, los cuales, serán añadidos a la lista con append.
            try:
                valor = int(input(f"Valor para posición [{f+1}, {c+1}]: "))
                if 0 <= valor <= 2: # Recuerda que el valor 1 es representado como □, el 2 como X y el 0 como un espacio vacío. 
                    # Para que la rerpresentación sea la deseada, debemos convertir los valores 0, 1 y 2 en sus símbolos correspondientes para luego hacer el append.
                    if valor == 0:
                        valor = " "
                    elif valor == 1:
                        valor = "□"
                    else:
                        valor = "X"
                    fila_actual.append(valor) # Añadimos el valor a la fila actual.
                    c += 1 
                else:
                    print("El valor debe estar entre 0 y 2.")
            except ValueError:
                print("Error: Debes introducir un número entero dentro de los parametros correspondientes.")

        matriz.append(fila_actual) # Añadimos la fila actual a la lista vacía "matriz" para que vaya tomando forma.
        if any("X" in fila for fila in matriz): # Si la matriz contiene al menos una X, entonces se devuelve la matriz con normalidad.
            return matriz    
    print("Error: La matriz debe contener al menos un personaje (X).") # Si no hubiera personaje entonces no tendría sentido el juego, por lo tanto, 
    # se enviará un mensaje de error y se pedirá al usuario que vuelva a introducir los valores.

# Función para encontrar el caracter "X" dentro de la matriz para luego devolver su posición en las variables f y c.
def encontrar_personaje(matriz):
    for f in range(len(matriz)): # Recorrer filas.
        for c in range(len(matriz[f])): # Recorrer columnas dentro de cada fila.
            if matriz[f][c] == "X": 
                return f, c # Esta función recorre la matriz hasta encontrar la posición de la X dentro de la matriz para luego devolverlo.
    return None, None

# Función para el movimiento (Asistencia de IA dentro de bibliografías).
def jugar_v2(matriz, f_act, c_act, file_path):
    """Bucle de juego optimizado: recibe y actualiza coordenadas."""
    while True:
        # Mostrar mapa
        print("\n" + "="*20)
        for fila in matriz:
            print(" ".join(fila)) # Imprime la matriz en la consola.
        
        accion = input("\nMover (W/A/S/D) o (Q) Salir: ").upper()
        if accion == "Q": break
        
        # Calcular destino potencial
        f_sig, c_sig = f_act, c_act
        if accion == "W": f_sig -= 1
        elif accion == "S": f_sig += 1
        elif accion == "A": c_sig -= 1
        elif accion == "D": c_sig += 1
        else: continue

        # Validaciones (Límites y Paredes)
        if 0 <= f_sig < len(matriz) and 0 <= c_sig < len(matriz[0]):
            if matriz[f_sig][c_sig] != "□":
                # ACTUALIZACIÓN EN MEMORIA
                matriz[f_act][c_act] = " "  # Borra rastro
                matriz[f_sig][c_sig] = "X"    # Nueva posición
                
                # Actualizar coordenadas para el siguiente turno
                f_act, c_act = f_sig, c_sig
                
                # ACTUALIZACIÓN EN DISCO (Guardado automático)
                crear_archivo(file_path, matriz)
            else:
                print("¡Muro detectado!")
        else:
            print("¡Límite del mapa!")


# Llamamos a las funciones para que el código comience a funcionar.
matriz_file_path = "data/raw/matriz_data.txt"
matriz_data = cargar_matriz(matriz_file_path) # Cargamos la matriz desde el archivo, si es que existe, para no perder los datos previos.
if matriz_data is None: # Si no existe, entonces debemos de crear la matriz desde cero, así que llamamos a las funciones correspondientes.
    f = crear_filas()
    c = crear_columnas()
    matriz_data = rellenar_matriz(f, c)
    crear_archivo(matriz_file_path, matriz_data)
else: 
    print( "Mapa cargado con éxito.")

fila_inicio, col_inicio = encontrar_personaje(matriz_data) # La posición de la x quedará guardada dentro de esas variables para luego ser utilizada en la función jugar_v2.

if fila_inicio is not None: # Si la función encuentra a la x con éxito, entonces se ejecutará la función responsable del movimiento del personaje.
    jugar_v2(matriz_data, fila_inicio, col_inicio, matriz_file_path)
else:
    print("Error: No se encontró al personaje (X) en el mapa.")
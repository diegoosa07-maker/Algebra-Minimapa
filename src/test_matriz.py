# IMPORTANTE: Gran parte del código presente en este archivo pertence a nuestras clases de fundamentos de programación, es decir, parte del mismo
# es reciclado de clases anteriores. Aunque este sea el caso, el código cuenta con retoques propios y otras modificaciones, así como la 
# asistencia de Gemini para solucionar problemas menores como tabulación o conversión de json a formato txt. (Conversación en Pdf)

import os 
import json 

def crear_archivo(file_path, matriz, mode='w'):
    # Creamos la carpeta si no existe
    os.makedirs(os.path.dirname(file_path), exist_ok=True) # Reescribimos el archivo para cada vez que vayamos a modificar la matriz, podríamos
    with open(file_path, mode, encoding="utf-8") as f:     # no hacer esto y simplemente ir añadiendo matrices pero el archivo se llenaría.
        for fila in matriz:
            # Convertimos cada número dentro de cada fila a string y los unimos con espacios, esta linea inferior es la más influenciada por IA.
            linea = " ".join(map(str, fila)) # map convierte lo que haya en el parametro de la izquierda a lo que haya al formato de la derecha
            f.write(linea + "\n") # Escribimos la fila y un salto de línea

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
    matriz = [] # Actualmente la matriz se encuentra vacía, no será hasta main que recivirá los valores de las filas y las columnas, pero hasta
    # entonces podemos ir atribuyendo valores a las posiciones de la matriz.
    print(f"\nIntroduce valores de 0 a 100 para una matriz de {filas}x{columnas}") 
    for f in range(filas):
        fila_actual = [] # Esta lista contendrá los valores de los números en cada fila.
        c = 0
        while c < columnas: # En este bucle es dónde creamos los valores dentro de la lista fila_actual, los cuales, serán añadidos a la lista con append.
            try:
                valor = int(input(f"Valor para posición [{f+1}, {c+1}]: "))
                if 0 <= valor <= 100:
                    fila_actual.append(valor)
                    c += 1 
                else:
                    print("El valor debe estar entre 0 y 100.")
            except ValueError:
                print("Error: Debes introducir un número entero.")

        matriz.append(fila_actual) 
        
    return matriz 

# Llamamos a las funciones para que el código comience a funcionar.

filas = crear_filas()
columnas = crear_columnas()
matriz_data = rellenar_matriz(filas, columnas)
matriz_file_path = "data/raw/matriz_data.txt"
crear_archivo(matriz_file_path, matriz_data)
print(f"\nMatriz guardada con éxito en {matriz_file_path}")
print("Contenido de la matriz:", matriz_data)
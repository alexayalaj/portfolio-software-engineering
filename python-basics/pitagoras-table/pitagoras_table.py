# Tabla de Pitágoras 1..10 usando listas de listas
# - mostrar_tabla: solo imprime (no regresa valor)
# - producto: regresa el valor desde la matriz (sin usar '*')

def construir_tabla(n=10):
    """Crea la tabla de Pitágoras como lista de listas sin usar '*'."""
    matriz = []
    for i in range(1, n + 1):
        fila = []
        acumulado = 0
        for _ in range(n):
            acumulado += i      # sumas sucesivas: i, 2i, 3i, ...
            fila.append(acumulado)
        matriz.append(fila)
    return matriz

def mostrar_tabla(matriz):
    """Imprime la tabla alineada, sin corchetes ni comas."""
    n = len(matriz)
    ancho = len(str(n * n))  # ancho para alinear (p. ej. 100 -> 3)
    # Encabezado
    print(" " * (ancho + 2), end="")
    for j in range(1, n + 1):
        print(f"{j:>{ancho+1}}", end=" ")
    print()
    # Filas con etiqueta lateral
    for i, fila in enumerate(matriz, start=1):
        print(f"{i:>{ancho}} ", end="")
        for valor in fila:
            print(f"{valor:>{ancho+1}}", end=" ")
        print()

def producto(matriz, a, b):
    """Devuelve el 'producto' consultando la matriz (1-indexado)."""
    return matriz[a - 1][b - 1]

def pedir_factores(n):
    while True:
        try:
            a = int(input(f"Ingrese el primer factor (1..{n}): "))
            b = int(input(f"Ingrese el segundo factor (1..{n}): "))
            if 1 <= a <= n and 1 <= b <= n:
                return a, b
            print(f"Los factores deben estar entre 1 y {n}. Intenta de nuevo.")
        except ValueError:
            print("Entrada inválida. Usa números enteros.")

def main():
    n = 10                     # cambia este valor si quieres otra dimensión
    tabla = construir_tabla(n) # lista de listas
    mostrar_tabla(tabla)       # función que NO regresa valor
    a, b = pedir_factores(n)
    resultado = producto(tabla, a, b)  # función que SÍ regresa valor
    print(f"\nResultado: {a} × {b} = {resultado}")

if __name__ == "__main__":
    main()

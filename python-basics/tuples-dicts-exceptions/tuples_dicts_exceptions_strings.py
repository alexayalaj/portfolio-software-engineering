
"""
Aplicación: Fundamentos de Programación - Actividad 4
Estructuras: Tuplas, Diccionarios, Excepciones y Strings
Autor: Alexis Ayala
Descripción:
    Programa interactivo con menú que demuestra:
    - Uso de tuplas (creación, acceso, "agregado" vía captura, conversión y ordenamiento).
    - Función que suma valores de una tupla de números.
    - Uso de diccionarios (creación, inserción por entrada, recorrido, búsqueda por función).
    - Manejo de excepciones (captura de entradas no numéricas y excepción personalizada para división entre cero).
    - Uso de strings (longitud, mayúsculas, reemplazo, conteo de palabras por función).
"""

from typing import Tuple, Dict

# --------------------------
# Sección: Tuplas
# --------------------------
def sumar_tupla(numeros: Tuple[float, ...]) -> float:
    """
    Recibe una tupla de números y retorna la suma.

    :param numeros: tupla de valores numéricos (int/float)
    :return: suma de los elementos
    """
    # Validación simple: asegurar que todos sean numéricos
    total = 0.0
    for n in numeros:
        if not isinstance(n, (int, float)):
            raise TypeError("La tupla contiene elementos no numéricos.")
        total += n
    return total


def demo_tuplas():
    print("\n--- DEMO: Tuplas ---")

    # 1) Tupla "frutas" con al menos 5 elementos
    frutas = ("manzana", "plátano", "naranja", "uva", "fresa")
    print(f"Tupla original: {frutas}")

    # 2) Acceder al tercer elemento (índice 2)
    print(f"Tercer elemento: {frutas[2]}")

    # 3) "Agregar" dos frutas vía captura (tuplas son inmutables, así que creamos una nueva)
    nueva1 = input("Ingresa una fruta adicional: ").strip()
    nueva2 = input("Ingresa otra fruta adicional: ").strip()
    frutas_ext = frutas + (nueva1, nueva2)
    print(f"Tupla extendida (inmutable, nueva tupla): {frutas_ext}")

    # 4) Convertir a lista y ordenar alfabéticamente
    lista_frutas = list(frutas_ext)
    lista_frutas.sort(key=lambda s: s.casefold())  # orden alfabético sin distinguir mayúsculas/minúsculas
    print(f"Lista ordenada: {lista_frutas}")

    # 5) Función que suma tupla de números -> ya definida: sumar_tupla

    # 6) Aplicar la función a la tupla de frutas.
    #    Interpretación: sumaremos la longitud (cantidad de letras) de cada fruta.
    longitudes = tuple(len(f) for f in frutas_ext)
    total_letras = sumar_tupla(longitudes)
    print(f"Suma de longitudes de los nombres de frutas: {total_letras}")


# --------------------------
# Sección: Diccionarios
# --------------------------
def buscar_contacto(contactos: Dict[str, str], nombre: str) -> str | None:
    """
    Busca un contacto por nombre (clave) y retorna su teléfono si existe.

    :param contactos: diccionario {nombre: telefono}
    :param nombre: nombre a buscar (no sensible a mayúsculas/minúsculas)
    :return: número telefónico o None si no existe
    """
    # Búsqueda no sensible a mayúsculas/minúsculas
    nombre_normalizado = nombre.casefold()
    for k, v in contactos.items():
        if k.casefold() == nombre_normalizado:
            return v
    return None


def demo_diccionarios():
    print("\n--- DEMO: Diccionarios ---")

    # 1) Crear "contactos" con al menos 3 entradas
    contactos = {
        "Ana": "55-1234-5678",
        "Benito": "55-9876-5432",
        "Carla": "55-1111-2222",
    }
    print("Diccionario inicial:", contactos)

    # 2) Agregar un nuevo contacto vía captura
    nombre = input("Nombre del nuevo contacto: ").strip()
    telefono = input("Teléfono del nuevo contacto: ").strip()
    if nombre:
        contactos[nombre] = telefono
    print("Diccionario actualizado:", contactos)

    # 3) Iterar sobre claves e imprimir nombres
    print("Nombres de contactos:")
    for nombre_contacto in contactos.keys():
        print("-", nombre_contacto)

    # 4) Función buscar_contacto(contactos, nombre) -> ya definida

    # 5) Aplicar la función para buscar un número
    buscar = input("¿Qué contacto deseas buscar?: ").strip()
    numero = buscar_contacto(contactos, buscar)
    if numero is not None:
        print(f"Teléfono de {buscar}: {numero}")
    else:
        print(f"No se encontró el contacto '{buscar}'.")


# --------------------------
# Sección: Excepciones
# --------------------------
class DivisionEntreCeroError(Exception):
    """Excepción personalizada para división entre cero."""


def dividir(a: int, b: int) -> float:
    """Divide a entre b, lanzando una excepción personalizada si b == 0."""
    if b == 0:
        raise DivisionEntreCeroError("No es posible dividir entre cero.")
    return a / b


def demo_excepciones():
    print("\n--- DEMO: Excepciones ---")
    try:
        x = int(input("Ingresa el primer número entero: ").strip())
        y = int(input("Ingresa el segundo número entero: ").strip())
    except ValueError:
        print("Error: Debes ingresar valores numéricos enteros válidos.")
        return

    # 3) Si son numéricos, mostrar la suma
    print(f"Suma: {x} + {y} = {x + y}")

    # 4) Intentar una división y manejar división entre cero con excepción personalizada
    try:
        resultado = dividir(x, y)
    except DivisionEntreCeroError as e:
        print(f"Error de división: {e}")
    else:
        print(f"División: {x} / {y} = {resultado}")


# --------------------------
# Sección: Strings
# --------------------------
def contar_palabras(texto: str) -> int:
    """
    Cuenta cuántas palabras contiene un string.
    Se separa por espacios en blanco (split sin argumentos).
    """
    return len(texto.split())


def demo_strings():
    print("\n--- DEMO: Strings ---")

    # 1) Variable mensaje (texto de mi elección)
    mensaje = "La programación en Python es divertida y poderosa."
    print("Mensaje:", mensaje)

    # 2) Longitud del mensaje
    print("Longitud del mensaje:", len(mensaje))

    # 3) Convertir a mayúsculas (upper)
    print("En mayúsculas:", mensaje.upper())

    # 4) Reemplazar una palabra específica
    reemplazado = mensaje.replace("poderosa", "práctica")
    print("Reemplazo de palabra:", reemplazado)

    # 5) Función que cuente palabras -> contar_palabras
    # 6) Aplicar función al mensaje
    print("Cantidad de palabras en el mensaje:", contar_palabras(mensaje))


# --------------------------
# Menú principal
# --------------------------
def menu():
    while True:
        print("\n====== MENÚ PRINCIPAL ======")
        print("1) Uso de Tuplas")
        print("2) Uso de Diccionarios")
        print("3) Uso de Excepciones")
        print("4) Uso de Strings")
        print("0) Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            demo_tuplas()
        elif opcion == "2":
            demo_diccionarios()
        elif opcion == "3":
            demo_excepciones()
        elif opcion == "4":
            demo_strings()
        elif opcion == "0":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu()

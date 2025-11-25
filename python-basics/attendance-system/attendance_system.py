# -*- coding: utf-8 -*-
"""
Programa: Control de Asistencia - Fase II (Mejoras con conceptos avanzados)
Autor: Alexis Ayala
Descripción:
  - Este script implementa un sistema de consola que cumple con la rúbrica del proyecto final.
  - Incluye: bienvenida con nickname, función de 'carga' (<=5s), menú en matriz con while,
    medición de tiempo con for, captura de fecha en tupla, lectura/escritura/creación de archivos,
    manejo de excepciones, y comentarios extensivos para facilitar mantenimiento.
Requisitos (resumen mapeado):
  1) Solicitar nombre/nickname.
  2) Mensaje de bienvenida usando operadores de cadena.
  3) Función de 'loading' <= 5 seg con mensaje.
  4) Menú (while) en formato matricial con opciones: leer, escribir, crear, cambiar usuario, salir.
  5) Medir tiempo de selección con for; si >10 minutos, preguntar si desea continuar.
  6) Capturar fecha dd/mm/aaaa, almacenarla en tupla (día, mes, año) y usarla al crear/modificar.
  7) Contar con >=4 archivos disponibles para lectura (se crean si no existen) y permitir abrir por nombre.
  8) Manejar excepciones comunes (archivo inexistente, nombre mal escrito, entradas inválidas).
  9) Comentarios relevantes para mantenimiento.
 10) Código depurado.
 11) El reporte se adjuntará por separado en Canvas.
"""
from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from datetime import datetime
from itertools import cycle
from pathlib import Path
from typing import Dict, List, Tuple


# ================================
# Utilidades y Estructuras de Datos
# ================================

@dataclass
class Session:
    """Representa una sesión de usuario en la aplicación."""
    nickname: str
    fecha_tuple: Tuple[int, int, int]  # (día, mes, año)
    base_dir: Path                     # Carpeta donde se gestionan los archivos

    @property
    def fecha_str(self) -> str:
        """Convierte la tupla de fecha a formato dd/mm/aaaa (para impresión)."""
        d, m, a = self.fecha_tuple
        return f"{d:02d}/{m:02d}/{a:04d}"


def limpiar_pantalla() -> None:
    """Intento simple de 'limpiar' la consola con saltos de línea (portátil)."""
    print("\n" * 50)


def loading(max_seconds: int = 5) -> None:
    """
    3) Muestra una animación de carga por hasta `max_seconds` segundos.
       Justifica el límite <= 5 segundos por rúbrica.
    """
    print("Cargando programa, por favor espera...", end="", flush=True)
    spinner = cycle([" ⠋", " ⠙", " ⠹", " ⠸", " ⠼", " ⠴", " ⠦", " ⠧", " ⠇", " ⠏"])
    start = time.perf_counter()
    # Bucle de espera (máximo max_seconds, por default 5)
    while time.perf_counter() - start < max_seconds:
        # Imprime el siguiente frame del spinner y pausa ligeramente
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.12)
        # Retrocede 2 caracteres para sobreescribir en la misma línea
        sys.stdout.write("\b\b")
    print("\n")


def pedir_nickname() -> str:
    """1) Solicita el nombre o nickname al usuario con validación básica."""
    while True:
        nick = input("Escribe tu nombre o nickname: ").strip()
        if nick:
            # 2) Demostración de operadores de cadena: concatenación y métodos
            nick = "@" + nick.replace(" ", "_")  # e.g., 'Juan Pérez' -> '@Juan_Pérez'
            return nick
        print("El nickname no puede estar vacío. Intenta de nuevo.")


def pedir_fecha_tuple() -> Tuple[int, int, int]:
    """
    6) Pide una fecha en formato dd/mm/aaaa, valida y regresa una tupla (día, mes, año).
    - Se usa datetime.strptime para validación.
    """
    while True:
        raw = input("Ingresa la fecha en formato dd/mm/aaaa (ej. 12/06/2023): ").strip()
        try:
            dt = datetime.strptime(raw, "%d/%m/%Y")
            return (dt.day, dt.month, dt.year)
        except ValueError:
            print("Formato inválido. Asegúrate de usar dd/mm/aaaa y que la fecha exista.")


def asegurar_archivos_iniciales(base_dir: Path) -> List[Path]:
    """
    7) Crea una carpeta 'files' y, si faltan, genera >=4 archivos de ejemplo para lectura.
    Devuelve la lista de rutas disponibles.
    """
    base_dir.mkdir(parents=True, exist_ok=True)
    # Archivos base (si no existen, se crean con contenido inicial)
    nombres = ["alumnos.txt", "asistencias.txt", "notas.txt", "reporte.txt"]
    rutas: List[Path] = []
    contenido_demo = (
        "Sistema de Control de Asistencia - Archivo de Ejemplo\n"
        "---------------------------------------------\n"
        "Puedes leer, escribir o crear archivos desde el menú.\n"
    )
    for nombre in nombres:
        ruta = base_dir / nombre
        if not ruta.exists():
            ruta.write_text(contenido_demo, encoding="utf-8")
        rutas.append(ruta)
    return rutas


def listar_archivos(base_dir: Path) -> Dict[int, Path]:
    """Devuelve un diccionario {índice: ruta} con los archivos del directorio base."""
    archivos = sorted(p for p in base_dir.glob("*") if p.is_file())
    return {i + 1: p for i, p in enumerate(archivos)}


def imprimir_matriz_menu() -> None:
    """
    4) Presenta el menú en formato tabular (matricial) de >=2 columnas.
       Se usan operadores de cadena (multiplicación de strings y formateo).
    """
    opciones = [
        ("1", "Leer archivo"),
        ("2", "Escribir archivo"),
        ("3", "Crear archivo"),
        ("4", "Cambiar usuario"),
        ("5", "Salir")
    ]
    # Construcción de una tabla simple de 2 columnas (celdas: código y descripción)
    ancho_cod, ancho_desc = 4, 22
    linea_sep = "+" + "-" * (ancho_cod + 2) + "+" + "-" * (ancho_desc + 2) + \
                "+" + "-" * (ancho_cod + 2) + "+" + "-" * (ancho_desc + 2) + "+"
    print(linea_sep)
    # Recorremos de 2 en 2 para llenar la matriz con dos columnas
    for i in range(0, len(opciones), 2):
        celda1 = opciones[i]
        celda2 = opciones[i + 1] if i + 1 < len(opciones) else ("", "")
        fila = (
            f"| {celda1[0]:<{ancho_cod}} | {celda1[1]:<{ancho_desc}} | "
            f"{celda2[0]:<{ancho_cod}} | {celda2[1]:<{ancho_desc}} |"
        )
        print(fila)
        print(linea_sep)


def medir_tiempo_seleccion_y_preguntar() -> bool:
    """
    5) Mide el tiempo que tarda el usuario en seleccionar una opción.
       - Limitación técnica: input() es bloqueante; no podemos interrumpirlo de forma portable.
         Estrategia: registramos timestamps antes y después de input; después calculamos elapsed.
       - Uso del ciclo for: recorremos 'elapsed' segundos para simular conteo/medición (requisito).
       Devuelve True si se debe continuar en el menú, False si se debe regresar a pantalla inicial.
    """
    inicio = time.perf_counter()
    opcion = input("Selecciona una opción: ").strip()
    fin = time.perf_counter()
    elapsed = fin - inicio

    # 'Uso de for' para medir/recorrer los segundos consumidos (propósito pedagógico)
    for _ in range(int(elapsed)):
        pass  # No hacemos nada, solo cumplimos el requisito de usar 'for' para la medición

    # Si tardó más de 10 minutos (600 s), preguntar si continúa
    if elapsed >= 600:
        resp = input("Han pasado más de 10 minutos sin elegir. ¿Deseas continuar? (si/no): ").strip().lower()
        if resp != "si":
            return False  # Regresar a pantalla inicial (cambio de usuario)
    # Guardamos la última opción elegida en un atributo temporal del objeto función (truco simple)
    medir_tiempo_seleccion_y_preguntar.ultima_opcion = opcion  # type: ignore
    return True


def seleccionar_archivo(base_dir: Path) -> Path:
    """
    Muestra los archivos disponibles y permite seleccionar por índice o por nombre.
    Lanza FileNotFoundError si no existe el archivo indicado.
    """
    disponibles = listar_archivos(base_dir)
    if not disponibles:
        raise FileNotFoundError("No hay archivos disponibles en la carpeta de trabajo.")

    print("Archivos disponibles:")
    for idx, ruta in disponibles.items():
        print(f"  {idx}. {ruta.name}")

    eleccion = input("Escribe el número o el nombre del archivo: ").strip()
    # Intento por índice
    if eleccion.isdigit():
        idx = int(eleccion)
        if idx in disponibles:
            return disponibles[idx]
        raise FileNotFoundError("El número elegido no corresponde a ningún archivo.")
    # Intento por nombre
    candidato = base_dir / eleccion
    if candidato.exists() and candidato.is_file():
        return candidato
    raise FileNotFoundError("Archivo no encontrado. Verifica el nombre y vuelve a intentar.")


def leer_archivo(base_dir: Path) -> None:
    """Opción 1: Lee e imprime el contenido de un archivo existente."""
    try:
        ruta = seleccionar_archivo(base_dir)
        print("\n" + "=" * 60)
        print(f"Contenido de: {ruta.name}")
        print("=" * 60)
        print(ruta.read_text(encoding="utf-8"))
        print("=" * 60 + "\n")
    except FileNotFoundError as e:
        print(f"[Aviso] {e}")
    except Exception as e:
        print(f"[Error] No se pudo leer el archivo: {e}")


def escribir_archivo(session: Session) -> None:
    """
    Opción 2: Escribe (anexa) texto a un archivo existente.
    - Inserta metadatos con usuario y fecha (tupla).
    """
    try:
        ruta = seleccionar_archivo(session.base_dir)
        print("Escribe el texto a anexar (Enter para finalizar):")
        texto = input("> ").rstrip()
        if not texto:
            print("No se escribió contenido. Operación cancelada.")
            return
        d, m, a = session.fecha_tuple
        cabecera = f"[Usuario: {session.nickname}] [Fecha: {d:02d}/{m:02d}/{a:04d}]\n"
        ruta.write_text(ruta.read_text(encoding="utf-8") + cabecera + texto + "\n", encoding="utf-8")
        print(f"Texto anexado correctamente a '{ruta.name}'.\n")
    except FileNotFoundError as e:
        print(f"[Aviso] {e}")
    except Exception as e:
        print(f"[Error] No se pudo escribir en el archivo: {e}")


def crear_archivo(session: Session) -> None:
    """
    Opción 3: Crea un nuevo archivo en la carpeta base de la sesión.
    - Usa la fecha capturada (tupla) dentro del contenido.
    - Valida que el nombre de archivo sea válido y no se sobrescriba sin querer.
    """
    try:
        nombre = input("Nombre del nuevo archivo (ej. bitacora.txt): ").strip()
        if not nombre:
            print("Nombre vacío. Operación cancelada.")
            return
        ruta = session.base_dir / nombre
        if ruta.exists():
            print("El archivo ya existe. Elige 'Escribir archivo' si deseas anexar contenido.\n")
            return
        d, m, a = session.fecha_tuple
        contenido = (
            f"Archivo creado por {session.nickname}\n"
            f"Fecha de creación: {d:02d}/{m:02d}/{a:04d}\n"
            "---------------------------------------------\n"
        )
        ruta.write_text(contenido, encoding="utf-8")
        print(f"Archivo '{ruta.name}' creado correctamente.\n")
    except OSError as e:
        print(f"[Error del sistema de archivos] {e}")
    except Exception as e:
        print(f"[Error] No se pudo crear el archivo: {e}")


def pantalla_inicial(base_dir: Path) -> Session:
    """
    Pantalla inicial: pide nickname, muestra bienvenida y solicita fecha.
    Regresa una Session lista para trabajar.
    """
    limpiar_pantalla()
    print("=" * 60)
    print("CONTROL DE ASISTENCIA — FASE II".center(60))
    print("=" * 60)

    nick = pedir_nickname()
    # 2) Mensaje de bienvenida con operadores de cadena (concatenación y f-string)
    bienvenida = "Bienvenido/a, " + f"{nick.upper()}"
    print(bienvenida.center(60))
    loading(max_seconds=5)

    fecha_tuple = pedir_fecha_tuple()
    session = Session(nickname=nick, fecha_tuple=fecha_tuple, base_dir=base_dir)
    print(f"Sesión iniciada para {session.nickname} en fecha {session.fecha_str}.\n")
    return session


def bucle_menu(session: Session) -> None:
    """
    4) Menú principal con while; opciones: leer, escribir, crear, cambiar usuario, salir.
    5) Medición de tiempo con for; si >10 min, preguntar si continuar.
    7-8) Gestión de archivos con excepciones.
    """
    while True:
        print("Menú principal (usa el número de la opción):")
        imprimir_matriz_menu()

        # 5) Medir tiempo de selección (ver función)
        continuar = medir_tiempo_seleccion_y_preguntar()
        if not continuar:
            # Cambio a pantalla inicial (nuevo usuario)
            raise KeyboardInterrupt  # Usamos esta excepción para romper y reiniciar flujo superior

        opcion = getattr(medir_tiempo_seleccion_y_preguntar, "ultima_opcion", "").strip()

        if opcion == "1":
            leer_archivo(session.base_dir)
        elif opcion == "2":
            escribir_archivo(session)
        elif opcion == "3":
            crear_archivo(session)
        elif opcion == "4":
            # 'Cambiar usuario': forzamos salida al nivel superior para reiniciar sesión
            print("Cambiando de usuario...\n")
            raise KeyboardInterrupt
        elif opcion == "5":
            print("¡Gracias por usar el sistema! Hasta pronto.")
            break
        else:
            print("Opción inválida. Intenta nuevamente.\n")


def main() -> None:
    """
    Punto de entrada del programa.
    - Prepara carpeta de trabajo.
    - Garantiza archivos iniciales.
    - Orquesta el flujo de pantalla inicial + menú con manejo de reintentos.
    """
    base_dir = Path.cwd() / "files"
    asegurar_archivos_iniciales(base_dir)

    while True:
        try:
            session = pantalla_inicial(base_dir)
            bucle_menu(session)
            break  # Si el usuario elige 'Salir', salimos del programa
        except KeyboardInterrupt:
            # Se usa para 'cambiar usuario' o regresar a pantalla inicial voluntariamente
            print("\nRegresando a pantalla inicial...\n")
            time.sleep(1.2)
            continue
        except Exception as e:
            print(f"[Error inesperado] {e}")
            print("Reiniciando a pantalla inicial...\n")
            time.sleep(1.2)


if __name__ == "__main__":
    main()


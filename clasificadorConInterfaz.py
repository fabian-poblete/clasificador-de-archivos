import os
import time
import tkinter as tk
from tkinter import filedialog
from threading import Thread

# Crear la ventana principal
root = tk.Tk()
root.title("Clasificador de Archivos")

# Establecer el ícono de la ventana
icon_path = "C:/Users/usuario/Desktop/Proyectos/Clasificador de archivos/icono.ico"  # Reemplaza con la ruta de tu archivo de ícono
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

# Función para centrar la ventana en la pantalla
def centrar_ventana():
    ancho_ventana = 500
    alto_ventana = 300
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()
    x = (ancho_pantalla - ancho_ventana) // 2
    y = (alto_pantalla - alto_ventana) // 2
    root.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

# Centrar la ventana en la pantalla
centrar_ventana()

# Variable global para almacenar el directorio seleccionado
directorio = None

# Función para manejar el evento de clic del botón
def seleccionar_directorio():
    global directorio
    # Abrir un cuadro de diálogo para seleccionar el directorio
    directorio_seleccionado = filedialog.askdirectory()
    if directorio_seleccionado:
        if directorio is None:
            # Primera vez seleccionando el directorio
            # Actualizar la variable de directorio
            directorio = directorio_seleccionado
            # Mostrar el directorio seleccionado en el widget de texto
            etiqueta_directorio.config(text=f"Directorio seleccionado: {directorio}")
            # Deshabilitar el botón de selección y habilitar el botón de cambio
            boton_seleccionar.config(text='Cambiar Directorio')
        else:
            # Cambiando el directorio
            # Limpiar el widget de texto
            texto_salida.delete(1.0, tk.END)
            # Actualizar la variable de directorio
            directorio = directorio_seleccionado
            # Mostrar el directorio seleccionado en el widget de texto
            etiqueta_directorio.config(text=f"Directorio seleccionado: {directorio}")
        # Clasificar todos los archivos existentes en el directorio
        clasificar_archivos_en_directorio()
        # Comenzar a monitorear el directorio en un hilo separado
        hilo = Thread(target=monitorear_directorio)
        hilo.start()

# Crear un botón para seleccionar/cambiar el directorio
boton_seleccionar = tk.Button(root, text='Seleccionar Directorio', command=seleccionar_directorio)
boton_seleccionar.pack()

# Crear una etiqueta para mostrar el directorio seleccionado
etiqueta_directorio = tk.Label(root, text="Directorio seleccionado: Ninguno")
etiqueta_directorio.pack()

# Crear un widget de texto para mostrar la salida
texto_salida = tk.Text(root, height=10, width=50)
texto_salida.pack()

# Función para clasificar un archivo
def clasificar_archivo(nombre_archivo):
    # Encontrar la extensión del archivo
    extension = nombre_archivo.split('.')[-1]

    # Iterar sobre las categorías
    for categoria, extensiones in categorias.items():
        # Si la extensión coincide con alguna de las extensiones de la categoría, mover el archivo
        if extension in extensiones:
            # Construir las rutas de archivo
            ruta_origen = os.path.join(directorio, nombre_archivo)
            ruta_destino_directorio = os.path.join(directorio, categoria)
            ruta_destino = os.path.join(ruta_destino_directorio, nombre_archivo)

            # Crear el directorio de destino si no existe
            if not os.path.exists(ruta_destino_directorio):
                os.makedirs(ruta_destino_directorio)

            # Mover el archivo
            os.rename(ruta_origen, ruta_destino)
            texto_salida.insert(tk.END, f'Se movió {nombre_archivo} a {categoria}\n')
            break

# Función para clasificar todos los archivos existentes en el directorio
def clasificar_archivos_en_directorio():
    # Limpiar el widget de texto
    texto_salida.delete(1.0, tk.END)
    for nombre_archivo in os.listdir(directorio):
        clasificar_archivo(nombre_archivo)

# Función para monitorear el directorio en busca de cambios
def monitorear_directorio():
    # Lista inicial de archivos en el directorio
    archivos_iniciales = os.listdir(directorio)

    while True:
        # Lista de archivos en el directorio después de una pausa corta
        time.sleep(1)
        archivos_actuales = os.listdir(directorio)

        # Encontrar los archivos nuevos
        archivos_nuevos = list(set(archivos_actuales) - set(archivos_iniciales))

        # Clasificar los archivos nuevos
        for nombre_archivo in archivos_nuevos:
            clasificar_archivo(nombre_archivo)

        # Actualizar la lista inicial de archivos
        archivos_iniciales = archivos_actuales

# Diccionario de categorías de archivos y sus extensiones
categorias = {
    'Imágenes': ['jpeg', 'jpg', 'png', 'jfif'],
    'PDFs': ['pdf'],
    'Conjuntos de datos': ['csv', 'xlsx', 'json'],
    'Videos': ['mp4'],
    'Documentos de Word': ['docx'],
    'Ejecutables': ['exe'],
    'Acceso directo': ['lnk'],
    'Gifs': ['gif'],
}

# Ejecutar el bucle principal de la ventana
root.mainloop()

import os
import time
import tkinter as tk
from tkinter import filedialog
from threading import Thread

# Crear la ventana principal
root = tk.Tk()
root.title("Clasificador de Archivos")

# Establecer el ícono de la ventana
icon_path = "C:/Users/usuario/Desktop/Clasificador de archivos/icono.ico"  # Reemplaza con la ruta de tu archivo de ícono
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

# Función para centrar la ventana en la pantalla
def centrar_ventana():
    ancho_ventana = 500
    alto_ventana = 500
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()
    x = (ancho_pantalla - ancho_ventana) // 2
    y = (alto_pantalla - alto_ventana) // 2
    root.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

# Centrar la ventana en la pantalla
centrar_ventana()

# Variable global para almacenar el directorio seleccionado
directorio = None
# Variable global para almacenar las categorías seleccionadas
categorias_seleccionadas = []

# Función para manejar el evento de clic del botón
def seleccionar_directorio():
    global directorio
    global categorias_seleccionadas
    # Restablecer las categorías seleccionadas
    categorias_seleccionadas = []
    
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

        # Mostrar los checkboxes de las categorías
        mostrar_checkboxes_categorias()

# Crear un botón para seleccionar/cambiar el directorio
boton_seleccionar = tk.Button(root, text='Seleccionar Directorio', command=seleccionar_directorio)
boton_seleccionar.pack(side=tk.TOP)

# Crear una etiqueta para mostrar el directorio seleccionado
etiqueta_directorio = tk.Label(root, text="Directorio seleccionado: Ninguno")
etiqueta_directorio.pack(side=tk.TOP)

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

# Lista para almacenar los checkboxes
checkboxes = []

# Función para mostrar los checkboxes de las categorías
def mostrar_checkboxes_categorias():
    global checkboxes

    # Limpiar el frame de categorías antes de volver a mostrar los checkboxes
    for checkbox, var in checkboxes:
        checkbox.pack_forget()
    checkboxes.clear()

    # Calcular el número de categorías por columna
    num_categorias = len(categorias)
    categorias_por_columna = (num_categorias + 1) // 2  # Redondeo hacia arriba

    # Crear los checkboxes de las categorías
    for i, (categoria, extensiones) in enumerate(categorias.items()):
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(frame_categorias, text=categoria, variable=var, onvalue=True, offvalue=False)
        checkbox.grid(row=i % categorias_por_columna, column=i // categorias_por_columna, sticky="w")
        checkboxes.append((checkbox, var))

# Crear un frame para los checkboxes de categorías
frame_categorias = tk.Frame(root)
frame_categorias.pack(side=tk.TOP)

# Crear un widget de texto para mostrar la salida
texto_salida = tk.Text(root, height=10, width=50)
texto_salida.pack(side=tk.TOP)

# Función para clasificar un archivo en la categoría correspondiente
def clasificar_archivo(nombre_archivo):
    # Encontrar la extensión del archivo
    extension = nombre_archivo.split('.')[-1]

    # Iterar sobre las categorías seleccionadas
    for checkbox, var in checkboxes:
        if var.get():
            categoria = checkbox.cget("text")
            extensiones = categorias[categoria]
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

# Función para realizar la clasificación de archivos al presionar el botón "Clasificar"
def clasificar_archivos():
    clasificar_archivos_en_directorio()

# Crear un botón para clasificar los archivos
boton_clasificar = tk.Button(root, text='Clasificar', command=clasificar_archivos)
boton_clasificar.pack(side=tk.TOP)

# Ejecutar el bucle principal de la ventana
root.mainloop()


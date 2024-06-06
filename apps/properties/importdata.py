import os
import pdb
from django.db import transaction

from apps.properties.models import Addenda

def importar_datos_desde_archivos():
    # Ruta a la carpeta que contiene los archivos de texto
    pdb.set_trace()
    ruta_carpeta = "c:\Proyectos\Canada\canada\database\data"

    # Listar archivos en la carpeta
    archivos = [archivo for archivo in os.listdir(ruta_carpeta) if archivo.endswith('.TXT')]

    for archivo in archivos:
        tabla_nombre = os.path.splitext(archivo)[0]  # Nombre de la tabla sin la extensión .txt

        with open(os.path.join(ruta_carpeta, archivo), 'r') as file:
            lineas = file.readlines()

            # Iterar sobre cada línea del archivo
            for linea in lineas:
                # Separar la información por comas
                datos = linea.strip().split(',')

                # Crear un diccionario con los nombres de los campos y sus valores
                campos_valores = dict(zip([campo.nombre for campo in Addenda._meta.fields], datos))

                # Crear un objeto de la tabla correspondiente y guardar en la base de datos
                with transaction.atomic():
                    try:
                        tabla = Addenda.objects.create(**campos_valores)
                    except Exception as e:
                        print(f"No se pudo guardar en la tabla {tabla_nombre}: {e}")

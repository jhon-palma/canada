import os
import pdb
import io
import csv

import shutil
from urllib import response
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from csv import reader

from django.apps import apps
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.contrib import messages
from django.db import transaction

from apps.properties.uploadData import create_objects, process_txt_data
from apps.users.views import user_verification
from .importdata import importar_datos_desde_archivos
from .forms import UploadFileForm
from .models import *
from datetime import datetime
from apps.users.models import Log
from immobilier.local_settings import PYTHON, PATH_BACKUP, PATH_BASE

import subprocess

def upload_file(request):
    mensaje = ''
    if request.method == 'POST':
     
        form = UploadFileForm(request.POST, request.FILES)
        txt_file = request.FILES['file']
        if not txt_file.name.lower().endswith('.txt'):
            messages.error(request, 'Invalid file type. Please upload a TXT file.')
            return  redirect('properties:upload_file')
        try:
            data = process_txt_data(txt_file)
            file_name = txt_file.name
            name_without_extension = file_name.split('.')[0]
            mensaje = create_objects(data, name_without_extension)
            messages.success(request, mensaje)
            Log.objects.create(
                usuario=request.user,
                modelo=name_without_extension,
                movimiento="CREATE",
                mensaje=mensaje
            )
            return redirect('properties:upload_file')
        except Exception as e:
            mensaje = f'Error processing TXT: {str(e)}'
            messages.error(request, mensaje )
            Log.objects.create(
                usuario=request.user,
                modelo=name_without_extension,
                movimiento="CREATE",
                mensaje=mensaje
            )
            return redirect('properties:upload_file')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html',{'form': form})

def upload_data_auto(request):
    mensaje = ''
    if request.method == 'POST':
        modelos = [
            'VALEURS_FIXES',
            'REGIONS',
            'MUNICIPALITES',
            'QUARTIERS',
            'TYPES_BANNIERES',
            'GENRES_PROPRIETES',
            'TYPE_CARACTERISTIQUES',
            'SOUS_TYPE_CARACTERISTIQUES',
            'FIRMES',
            'BUREAUX',
            'MEMBRES',
            'MEMBRES_MEDIAS_SOCIAUX',
            'INSCRIPTIONS',
            'PHOTOS',
            'LIENS_ADDITIONNELS',
            'VISITES_LIBRES',
            'REMARQUES',
            'UNITES_DETAILLEES',
            'ADDENDA',
            'UNITES_SOMMAIRES',
            'DEPENSES',
            'RENOVATIONS',
            'PIECES_UNITES',
            'CARACTERISTIQUES',
        ]
        folder_path = PATH_BASE

        try:
            
            for modelo in modelos:
                filename = modelo + '.txt'
                file_path = os.path.join(folder_path, filename)

                if os.path.exists(file_path):
                    data = process_txt_data(file_path)
                    name_without_extension = os.path.splitext(filename)[0]
                    mensaje = create_objects(data, name_without_extension)
                    messages.success(request, mensaje)
                    Log.objects.create(
                        usuario=request.user,
                        modelo=name_without_extension,
                        movimiento="CREATE",
                        mensaje=mensaje
                    )

                    if modelo == "MEMBRES":
                        mensaje = user_verification()
                        messages.error(request, mensaje)
                else:
                    messages.error(request, f'ERROR Archivo {filename} no encontrado.')
                    Log.objects.create(
                            usuario=request.user,
                            modelo=name_without_extension,
                            movimiento="CREATE",
                            mensaje=mensaje
                    )
                     
        except Exception as e:
            mensaje = f'Error processing files: {str(e)}'
            messages.error(request, mensaje)
            Log.objects.create(
                usuario=request.user,
                modelo="",
                movimiento="CREATE",
                mensaje=mensaje
            )
   
        return redirect('properties:upload_data_auto')
    return render(request, 'upload_auto.html')

def download_files(request):
    if request.method == 'POST':
        try:
            resultado = subprocess.run([PYTHON, "scripts/download_data.py"], capture_output=True, text=True, check=True)
            salida_del_script = resultado.stderr
            if salida_del_script:
                mensaje = f"Error al ejecutar el script: {salida_del_script}"
                messages.error(request, mensaje )
                Log.objects.create(
                    usuario=request.user,
                    modelo=" ",
                    movimiento="DOWNLOAD",
                    mensaje=mensaje
                )
                return redirect('properties:download_files')
            else:
                carpeta_origen = 'data/generic/'
                carpeta_destino = 'data'
                try:
                    for archivo in os.listdir(carpeta_origen):
                        print(archivo)
                        ruta_archivo_origen = os.path.join(carpeta_origen, archivo)
                        ruta_archivo_destino = os.path.join(carpeta_destino, archivo)
                        shutil.copy(ruta_archivo_origen, ruta_archivo_destino)
                    mensaje = "El script se ejecutó correctamente."
                    messages.success(request, mensaje)
                    Log.objects.create(
                        usuario=request.user,
                        modelo=" ",
                        movimiento="DOWNLOAD",
                        mensaje=mensaje
                    )
                    return redirect('properties:download_files')
                except Exception as e:
                    mensaje_error = "Error al copiar los archivos: {}".format(str(e))
                    messages.error(request, mensaje_error)
                    Log.objects.create(
                        usuario=request.user,
                        modelo= e ,
                        movimiento="DOWNLOAD",
                        mensaje=mensaje_error
                    )
                    return redirect('properties:download_files')
        except subprocess.CalledProcessError as e:
            mensaje =  f"Error al ejecutar el script: {e}"
            messages.error(request, mensaje )
            Log.objects.create(
                usuario=request.user,
                modelo=" ",
                movimiento="DOWNLOAD",
                mensaje=mensaje
            )
            return redirect('properties:download_files')
    return render(request, 'download.html')

def drop_database(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                user = request.user
                for modelo in ['Caracteristiques', 'PiecesUnites', 'Renovations', 'Depenses', 'UnitesSommaires', 'Addenda', 'UnitesDetaillees', 'Remarques', 'VisitesLibres', 'LiensAdditionnels', 'Photos', 'Inscriptions', 'MembresMediasSociaux', 'Membres', 'Bureaux', 'Firmes', 'SousTypeCaracteristiques', 'TypeCaracteristiques', 'GenresProprietes', 'TypesBannieres', 'Quartiers', 'Municipalites', 'Regions', 'ValeursFixes']:
                    Log.objects.create(
                    usuario=user,
                    modelo=modelo,
                    movimiento='Borrar',
                    mensaje='Se borraron todos los registros del modelo {}'.format(modelo)
                )
                models_drop = [
                    Caracteristiques,
                    PiecesUnites,
                    Renovations,
                    Depenses,
                    UnitesSommaires,
                    Addenda,
                    UnitesDetaillees,
                    Remarques,
                    VisitesLibres,
                    LiensAdditionnels,
                    Photos,
                    Inscriptions,
                    MembresMediasSociaux,
                    Membres,
                    Bureaux,
                    Firmes,
                    SousTypeCaracteristiques,
                    TypeCaracteristiques,
                    GenresProprietes,
                    TypesBannieres,
                    Quartiers,
                    Municipalites,
                    Regions,
                    ValeursFixes,
                ]
                total = 0
                for modelo in models_drop:
                    modelo.objects.all().delete()
                    total = total + 1 
                mensaje = "El script se ejecutó correctamente. {} modelos inicializados correctamente".format(total) 
                messages.success(request, mensaje)
                return redirect('properties:drop_database')
        except Exception as e:
            Log.objects.create(
                usuario=user,
                modelo='Error',
                movimiento='Error al borrar',
                mensaje=str(e)
            )
            mensaje =  f"Error al borrar: {e}"
            messages.error(request, mensaje )
            return redirect('properties:drop_database')
    return render(request, 'drop_database.html')
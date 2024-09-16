import django
from pathlib import Path
from ftplib import FTP
import re, os, zipfile
import sys 
import shutil
import datetime
from upload_data import create_objects, process_txt_data

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'immobilier.settings')
django.setup()

from immobilier.local_settings import FTP_IP, FTP_USER, FTP_PASSWORD
from apps.users.views import user_verification
from scripts.send_email import sendEmail

PATH_BASE = Path(__file__).resolve().parent.parent / 'data'
PATH_BACKUP = PATH_BASE / 'backups'

try:

    fecha_hora_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nueva_carpeta = '{}/Backup_{}'.format(PATH_BACKUP, fecha_hora_actual)
    os.makedirs(nueva_carpeta)

    for archivo in os.listdir(PATH_BASE):
        ruta_archivo = os.path.join(PATH_BASE, archivo)
        if os.path.isfile(ruta_archivo) and archivo.lower().endswith('.txt'):
            shutil.move(ruta_archivo, nueva_carpeta)

    ftp = FTP(FTP_IP)
    ftp.login(user=FTP_USER, passwd=FTP_PASSWORD)
    archivos = ftp.nlst()
    
    archivos_zip = [nombre for nombre in archivos if re.match(r'^COLUMBIATECHNOLOGY\d{8}\.zip$', nombre)]

    if archivos_zip:
        archivos_zip.sort(reverse=True)
        ultimo_archivo_zip = archivos_zip[0]
        print("ultimo archivo zip:", ultimo_archivo_zip)
        
        try: os.rmdir(PATH_BASE)
        except: pass
        
        with open(ultimo_archivo_zip, 'wb') as archivo_local:
            ftp.retrbinary('RETR ' + ultimo_archivo_zip, archivo_local.write)

        with zipfile.ZipFile(ultimo_archivo_zip, 'r') as archivo_zip:
            archivo_zip.extractall(PATH_BASE)  # Extraer archivos en la carpeta 'data'
        
        print("Archivo zip descargado y descomprimido correctamente.")
        os.remove(ultimo_archivo_zip)

        carpeta_origen = '{}/generic/'.format(PATH_BASE)
        carpeta_destino = PATH_BASE
        for archivo in os.listdir(carpeta_origen):
            ruta_archivo_origen = os.path.join(carpeta_origen, archivo)
            ruta_archivo_destino = os.path.join(carpeta_destino, archivo)
            shutil.copy(ruta_archivo_origen, ruta_archivo_destino)

        shutil.rmtree(nueva_carpeta)
    
    else:
        print("No se encontraron archivos zip en el directorio.")

    # Cerrar sesión
    ftp.quit()

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
    models_base = [
        'GENRES_PROPRIETES',
        'MUNICIPALITES',
        'QUARTIERS',
        'REGIONS',
        'SOUS_TYPE_CARACTERISTIQUES',
        'TYPE_CARACTERISTIQUES',
        'TYPES_BANNIERES',
        'VALEURS_FIXES'
    ]

    print("Cargando Datos")

    for modelo in modelos:
        filename = modelo + '.TXT' if modelo not in models_base else modelo + '.txt'
        file_path = os.path.join(folder_path, filename)

        if os.path.exists(file_path):
            data = process_txt_data(file_path)
            name_without_extension = os.path.splitext(filename)[0]
            mensaje = create_objects(data, name_without_extension)

            if modelo == "MEMBRES":
                user_verification()
                
    end = "Datos cargados correctamente."
    print(end)
    #sendEmail(content, 'icloudcris@gmail.com', 'crisdapu21@gmail.com')

except Exception as e:
    # Imprimir el error en la salida de errores estándar (stderr)
    print("Error:", e, file=sys.stderr)
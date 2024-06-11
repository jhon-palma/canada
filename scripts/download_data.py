from ftplib import FTP
import re, os, zipfile
import sys 
import shutil
import datetime

try:
    fecha_hora_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    nueva_carpeta = os.path.join('c:\Proyectos\Canada\Data', 'backups', 'Backup_' + fecha_hora_actual)

    os.makedirs(nueva_carpeta)

    for archivo in os.listdir('c:\Proyectos\Canada\Data'):
        ruta_archivo = os.path.join('c:\Proyectos\Canada\Data', archivo)
        if os.path.isfile(ruta_archivo) and archivo.lower().endswith('.txt'):
            shutil.move(ruta_archivo, nueva_carpeta)

    # Establecer conexión FTP
    # ftp = FTP('147.135.11.93')
    # ftp.login(user='ftplj', passwd='j1cVdVao1Pzb')
    ftp = FTP('135.148.26.180')
    ftp.login(user='ftplj', passwd='j1cVdVao1Pzb')

    # Obtener lista de archivos en el directorio remoto
    archivos = ftp.nlst()

    # Filtrar archivos zip con el patrón especificado
    archivos_zip = [nombre for nombre in archivos if re.match(r'^COLUMBIATECHNOLOGY\d{8}\.zip$', nombre)]

    if archivos_zip:
    
        # Ordenar archivos por fecha
        archivos_zip.sort(reverse=True)
        
        # Obtener el último archivo zip
        ultimo_archivo_zip = archivos_zip[0]
        print("ultimo archivo zip:", ultimo_archivo_zip)
        
        print(os.getcwd())
        
        try: os.rmdir('c:\Proyectos\Canada\Data')
        except: pass
        
        # Descargar el archivo zip
        with open(ultimo_archivo_zip, 'wb') as archivo_local:
            ftp.retrbinary('RETR ' + ultimo_archivo_zip, archivo_local.write)

        # Descomprimir el archivo zip
        with zipfile.ZipFile(ultimo_archivo_zip, 'r') as archivo_zip:
            archivo_zip.extractall('c:\Proyectos\Canada\Data')  # Extraer archivos en la carpeta 'data'
        
        print("Archivo zip descargado y descomprimido correctamente.")
        
        # Eliminar el archivo zip descargado
        os.remove(ultimo_archivo_zip)
    

    else:
        print("No se encontraron archivos zip en el directorio.")

    # Cerrar sesión
    ftp.quit()

except Exception as e:
    # Imprimir el error en la salida de errores estándar (stderr)
    print("Error:", e, file=sys.stderr)
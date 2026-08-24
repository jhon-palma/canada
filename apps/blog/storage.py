import posixpath
import uuid

from django.core.files.storage import Storage, default_storage


class CustomStorage(Storage):
    """Las imagenes que se insertan dentro del contenido de un articulo.

    django_ckeditor_5 llama a save() y devuelve lo que responda url(). Esto
    era un FileSystemStorage apuntando a MEDIA_ROOT: el archivo se guardaba en
    el disco del servidor y la URL quedaba en /media/..., que en produccion no
    sirve nadie (urls.py solo monta MEDIA_URL con DEBUG=True, y el dominio
    responde 403). La subida terminaba en 200 y la imagen insertada en el
    articulo estaba muerta, que es lo que se veia como "el editor no deja
    subir fotos".

    Ahora delega en el almacenamiento por defecto del proyecto -- Spaces en
    produccion, disco en desarrollo -- bajo el mismo prefijo `public/` que usan
    las portadas de los articulos. Ese prefijo es justo lo que mira
    MediaS3Boto3Storage._save para subirlas como public-read.
    """

    PREFIJO = 'public/web/blog/images/django_ckeditor_5'

    def _ruta(self, name):
        """Prefijo comun y un nombre que no pueda pisar a otro.

        MediaS3Boto3Storage tiene file_overwrite=True, asi que dos articulos
        que suban su 'captura.png' se sobrescribirian el uno al otro sin
        avisar. El identificador delante lo evita y deja el nombre original a
        la vista.
        """
        base = posixpath.basename(name.replace('\\', '/'))
        return posixpath.join(self.PREFIJO, '{}-{}'.format(uuid.uuid4().hex[:8], base))

    # -- lo que usa django_ckeditor_5 -------------------------------------

    def save(self, name, content, max_length=None):
        return default_storage.save(self._ruta(name), content, max_length=max_length)

    def url(self, name):
        return default_storage.url(name)

    # -- resto de la interfaz de Storage, por delegacion -------------------

    def open(self, name, mode='rb'):
        return default_storage.open(name, mode)

    def delete(self, name):
        return default_storage.delete(name)

    def exists(self, name):
        return default_storage.exists(name)

    def listdir(self, path):
        return default_storage.listdir(path)

    def size(self, name):
        return default_storage.size(name)

    def get_accessed_time(self, name):
        return default_storage.get_accessed_time(name)

    def get_created_time(self, name):
        return default_storage.get_created_time(name)

    def get_modified_time(self, name):
        return default_storage.get_modified_time(name)

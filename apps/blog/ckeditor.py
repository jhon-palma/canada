"""Subida de imagenes del editor, abierta a todo el equipo.

django_ckeditor_5 solo acepta la subida de un usuario con is_staff, y eso
dejaba fuera a casi todo el mundo: de las doce cuentas activas una sola lo
tiene. Publicar un articulo no deberia exigir acceso al admin de Django, asi
que aqui se aplica el mismo criterio que en el resto de la gestion del blog --
cuenta del equipo, userBlog=False -- y se reutiliza tal cual la maquinaria del
paquete para lo demas: el formulario que valida la extension, la verificacion
de que el archivo es una imagen de verdad y el almacenamiento configurado en
CKEDITOR_5_FILE_STORAGE.

El widget descubre esta vista por su nombre, con
CK_EDITOR_5_UPLOAD_FILE_VIEW_NAME en settings.
"""

from django.http import Http404, JsonResponse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from django_ckeditor_5.forms import UploadFileForm
from django_ckeditor_5.views import NoImageException, handle_uploaded_file, image_verify

from apps.decorators import interno_required


@interno_required
@require_POST
def upload_file(request):
    formulario = UploadFileForm(request.POST, request.FILES)

    archivo = request.FILES.get('upload')
    if archivo is None:
        raise Http404(_("Page not found."))

    try:
        image_verify(archivo)
    except NoImageException as error:
        return JsonResponse({"error": {"message": "{}".format(error)}}, status=400)

    if not formulario.is_valid():
        # Casi siempre la extension. Se devuelve el motivo en vez del 404 mudo
        # del paquete, que dejaba al editor diciendo solo "no se pudo subir".
        return JsonResponse(
            {"error": {"message": " ".join(formulario.errors.get('upload', []))}},
            status=400)

    return JsonResponse({"url": handle_uploaded_file(archivo)})

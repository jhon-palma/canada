from django.urls import path

from apps.decorators import staff_required
from . import views


# Todas estas vistas importan, reemplazan o borran la base de datos de
# inscripciones (drop_database vacia 24 modelos), por lo que quedan
# restringidas a usuarios internos con is_staff.
urlpatterns = [
    path('upload/', staff_required(views.upload_file), name='upload_file'),
    path('upload_auto/', staff_required(views.upload_data_auto), name='upload_data_auto'),
    path('download_files/', staff_required(views.download_files), name='download_files'),
    path('update_video_list/', staff_required(views.update_video_list), name='update_video_list'),
    path('drop_database/', staff_required(views.drop_database), name='drop_database'),
]

from django.urls import path
from . import views


urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('upload_auto/', views.upload_data_auto, name='upload_data_auto'),
    path('download_files/', views.download_files, name='download_files'),
    path('update_video_list/', views.update_video_list, name='update_video_list'),
    path('drop_database/', views.drop_database, name='drop_database'),
]
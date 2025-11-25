from django.urls import path
from . import views

urlpatterns = [
    path('', views.dispositivos_home, name='dispositivos_home'),
    path('<int:dispositivo_id>/', views.dispositivo_detalle, name='dispositivo_detalle'),
    path('<int:dispositivo_id>/editar/', views.dispositivo_editar, name='dispositivo_editar'),
    path('<int:dispositivo_id>/eliminar/', views.dispositivo_eliminar, name='dispositivo_eliminar'),
]
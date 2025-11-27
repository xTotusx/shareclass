from django.urls import path
from . import views

urlpatterns = [
    # Rutas CRUD básicas
    path('', views.dispositivos_home, name='dispositivos_home'),
    path('<int:dispositivo_id>/', views.dispositivo_detalle, name='dispositivo_detalle'),
    path('<int:dispositivo_id>/editar/', views.dispositivo_editar, name='dispositivo_editar'),
    path('<int:dispositivo_id>/eliminar/', views.dispositivo_eliminar, name='dispositivo_eliminar'),

    # NUEVAS RUTAS DE PRÉSTAMOS
    path('prestar/<int:dispositivo_id>/', views.prestar_dispositivo, name='prestar_dispositivo'),
    path('devolver/<int:prestamo_id>/', views.devolver_dispositivo, name='devolver_dispositivo'),
]
from django.urls import path
from . import views

urlpatterns = [
    # Vistas generales
    path('', views.libros_home, name='libros_home'),
    path('<int:libro_id>/', views.libro_detalle, name='libro_detalle'),
    path('<int:libro_id>/editar/', views.libro_editar, name='libro_editar'),
    path('<int:libro_id>/eliminar/', views.libro_eliminar, name='libro_eliminar'),
    
    # Nuevas rutas para Préstamos
    path('prestar/<int:libro_id>/', views.prestar_libro, name='prestar_libro'),
    path('devolver/<int:prestamo_id>/', views.devolver_libro, name='devolver_libro'),
]
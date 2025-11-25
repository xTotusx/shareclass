from django.urls import path
from . import views

urlpatterns = [
    path('', views.libros_home, name='libros_home'),
    path('<int:libro_id>/', views.libro_detalle, name='libro_detalle'),
    path('<int:libro_id>/editar/', views.libro_editar, name='libro_editar'),
    path('<int:libro_id>/eliminar/', views.libro_eliminar, name='libro_eliminar'), # Nueva ruta
]
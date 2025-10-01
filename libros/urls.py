from django.urls import path
from . import views

urlpatterns = [
    path('', views.libros_home, name='libros_home'),  # Página principal de libros
]


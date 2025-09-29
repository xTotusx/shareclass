from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),              # Página principal
    path('perfil/', views.perfil, name='perfil'),   # Página de perfil con selector de foto
    path('auth/', views.auth_view, name='auth'),    # Login y registro juntos
    path('logout/', views.logout_view, name='logout'), # Cerrar sesión
]

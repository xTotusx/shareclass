from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),        # Página pública
    path('home/', views.home, name='home'),         # Página principal (requiere login)
    path('auth/', views.auth_view, name='auth'),    # Login / registro
    path('perfil/', views.perfil, name='perfil'),   # Perfil de usuario
    path('logout/', views.logout_view, name='logout'),  # Cerrar sesión
]

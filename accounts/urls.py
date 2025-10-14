from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),          # 👈 Página inicial pública
    path('auth/', views.auth_view, name='auth'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('perfil/', views.perfil, name='perfil'),
]

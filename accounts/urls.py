from django.urls import path
from . import views

urlpatterns = [
    # Páginas normales
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('auth/', views.auth_view, name='auth'),
    path('perfil/', views.perfil, name='perfil'),
    path('logout/', views.logout_view, name='logout'),

    # Panel de administración
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'), # Corregido: apunta a admin_dashboard
    path('usuarios/', views.user_list, name='user_list'),
    path('cambiar-rol/<int:user_id>/', views.change_role, name='change_role'),
    path('eliminar/<int:user_id>/', views.delete_user, name='delete_user'),
]
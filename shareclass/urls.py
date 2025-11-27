"""
URL configuration for shareclass project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# ==========================================
# VISTA TEMPORAL PARA DARTE PODERES DE ADMIN
# ==========================================
@login_required
def hacerme_admin(request):
    try:
        # 1. Obtenemos al usuario que está logueado actualmente (TÚ)
        user = request.user
        
        # 2. Le damos permisos de Django (Superusuario)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        
        # 3. Le damos rol de 'admin' en el perfil (para tu Dashboard)
        if hasattr(user, 'profile'):
            user.profile.role = 'admin'
            user.profile.save()
            
        return HttpResponse(f"""
            <div style='font-family:sans-serif; text-align:center; padding:50px;'>
                <h1 style='color:green;'>✅ ¡ÉXITO!</h1>
                <p>El usuario <strong>{user.username}</strong> ahora es ADMINISTRADOR.</p>
                <br>
                <a href='/' style='background:#185a9d; color:white; padding:10px 20px; text-decoration:none; border-radius:5px;'>
                    Volver al Inicio
                </a>
            </div>
        """)
    except Exception as e:
        return HttpResponse(f"❌ Error: {e}")


# ==========================================
# RUTAS DEL SISTEMA
# ==========================================
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rutas de tus Apps
    path('', include('accounts.urls')),
    path('libros/', include('libros.urls')),
    path('dispositivos/', include('dispositivos.urls')),
    
    # PWA: Servir el manifest y service worker desde la raíz
    path('manifest.json', TemplateView.as_view(template_name='accounts/manifest.json', content_type='application/json'), name='manifest'),
    path('service-worker.js', TemplateView.as_view(template_name='accounts/service-worker.js', content_type='application/javascript'), name='service-worker'),
    
    # RUTA MÁGICA (Bórrala después de usarla)
    path('super-poderes/', hacerme_admin), 
]

# Configuración para servir imágenes (media) en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
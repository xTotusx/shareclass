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
from django.views.generic import TemplateView # Importante para el Service Worker


def crear_admin_emergencia(request):
    try:
        # Verifica si ya existe para no dar error
        if not User.objects.filter(username='admin').exists():
            # Crea usuario: admin / email / admin123
            User.objects.create_superuser('admin', 'admin@shareclass.com', 'admin123')
            return HttpResponse("✅ ÉXITO: Usuario 'admin' creado. Contraseña: 'admin123'")
        else:
            return HttpResponse("ℹ️ AVISO: El usuario 'admin' ya existía.")
    except Exception as e:
        return HttpResponse(f"❌ ERROR: {e}")


urlpatterns = [
    path('admin/', admin.site.urls),
    
    

    # Rutas de tus Apps
    path('', include('accounts.urls')),
    path('libros/', include('libros.urls')),
    path('dispositivos/', include('dispositivos.urls')),
    
    # PWA: Servir el manifest y service worker desde la raíz
    path('manifest.json', TemplateView.as_view(template_name='accounts/manifest.json', content_type='application/json'), name='manifest'),
    path('service-worker.js', TemplateView.as_view(template_name='accounts/service-worker.js', content_type='application/javascript'), name='service-worker'),
    path('setup-admin/', crear_admin_emergencia), # <--- ESTA ES LA URL MÁGICA
]

# Configuración para servir imágenes (media) en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
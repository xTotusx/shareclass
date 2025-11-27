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
# Importaciones para el diagnóstico
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse

# ==========================================
# VISTA DE DIAGNÓSTICO (Espía de configuración)
# ==========================================
def diagnostico(request):
    try:
        # 1. ¿Qué motor está usando Django realmente?
        motor = str(default_storage)
        # 2. ¿Qué dice el settings.py?
        backend = getattr(settings, 'DEFAULT_FILE_STORAGE', 'No definido')
        
        # 3. Prueba de fuego: Intentar subir un archivo real a la nube ahora mismo
        content = ContentFile(b'Prueba de conexion con Cloudinary desde Railway')
        file_name = default_storage.save('test_cloudinary.txt', content)
        file_url = default_storage.url(file_name)
        
        html = f"""
        <div style="font-family: monospace; padding: 20px;">
            <h1 style="color: #185a9d;">Diagnóstico de Archivos</h1>
            <p><strong>Backend en Settings:</strong> {backend}</p>
            <p><strong>Motor Activo en Memoria:</strong> {motor}</p>
            <hr>
            <h3>Prueba de Escritura:</h3>
            <p>✅ Archivo 'test_cloudinary.txt' guardado exitosamente.</p>
            <p><strong>URL Generada:</strong> <a href="{file_url}" target="_blank">{file_url}</a></p>
            <p style="color: gray;">(Si la URL empieza con http://res.cloudinary.com... ¡Funciona!)</p>
            <p style="color: gray;">(Si la URL empieza con /media/... Seguimos usando local)</p>
        </div>
        """
        return HttpResponse(html)
    except Exception as e:
        return HttpResponse(f"<h1 style='color:red'>Error Crítico:</h1><pre>{e}</pre>")


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rutas de tus Apps
    path('', include('accounts.urls')),
    path('libros/', include('libros.urls')),
    path('dispositivos/', include('dispositivos.urls')),
    
    # PWA: Servir el manifest y service worker desde la raíz
    path('manifest.json', TemplateView.as_view(template_name='accounts/manifest.json', content_type='application/json'), name='manifest'),
    path('service-worker.js', TemplateView.as_view(template_name='accounts/service-worker.js', content_type='application/javascript'), name='service-worker'),
    
    # RUTA DE DIAGNÓSTICO
    path('diagnostico/', diagnostico),
]

# Configuración para servir imágenes (media) en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
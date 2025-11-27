from django.db import models
from django.contrib.auth.models import User  # Importamos User
from django.utils import timezone            # Importamos timezone

class Dispositivo(models.Model):
    nombre = models.CharField(max_length=200)
    marca = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='dispositivos/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} - {self.marca}"

# ==========================================
# NUEVO MODELO: PRÉSTAMOS DE EQUIPOS
# ==========================================
class PrestamoDispositivo(models.Model):
    # Relación con el dispositivo
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name='prestamos')
    # Relación con el usuario
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prestamos_dispositivos')
    
    fecha_prestamo = models.DateTimeField(default=timezone.now)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)
    devuelto = models.BooleanField(default=False)

    def __str__(self):
        estado = "Devuelto" if self.devuelto else "En uso"
        return f"{self.dispositivo.nombre} - {self.usuario.username} ({estado})"
from django.db import models
from django.contrib.auth.models import User  # Necesario para vincular con el usuario
from django.utils import timezone            # Necesario para la fecha automática

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='libros/', blank=True, null=True)
    qr_code = models.ImageField(upload_to='libros_qr/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return f"{self.titulo} - {self.autor}"

# ==========================================
# NUEVO MODELO: SEGUIMIENTO DE PRÉSTAMOS
# ==========================================
class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='prestamos')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prestamos_libros')
    fecha_prestamo = models.DateTimeField(default=timezone.now)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)
    # devuelto=False significa que el usuario aún tiene el libro
    devuelto = models.BooleanField(default=False)

    def __str__(self):
        status = "Devuelto" if self.devuelto else "En posesión"
        return f"{self.libro.titulo} - {self.usuario.username} ({status})"
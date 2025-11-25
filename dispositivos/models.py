from django.db import models

class Dispositivo(models.Model):
    nombre = models.CharField(max_length=200) # Antes titulo
    marca = models.CharField(max_length=200)  # Antes autor
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='dispositivos/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} - {self.marca}"
from django.db import models

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='libros/', blank=True, null=True)
    qr_code = models.ImageField(upload_to='libros_qr/', blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} - {self.autor}"

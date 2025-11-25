from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('alumno', 'Alumno'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.CharField(max_length=100, default='avatar_pp1.jpeg')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='alumno')

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# ==========================
#   SEÑALES PARA CREAR PERFIL
# ==========================

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

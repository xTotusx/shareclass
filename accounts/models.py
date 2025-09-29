from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.CharField(
        max_length=100,
        choices=[
            ('avatar_pp1.jpeg', 'Avatar 1'),
            ('avatar_pp2.jpeg', 'Avatar 2'),
            ('avatar_pp3.jpeg', 'Avatar 3'),
            ('avatar_pp4.jpeg', 'Avatar 4'),
        ],
        default='avatar_pp1.jpeg'
    )

    def __str__(self):
        return f"Perfil de {self.user.username}"

# Crear perfil automáticamente al registrar un usuario
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name='О себе')
    avatar = models.ImageField(upload_to='profile/avatars/%Y/%m/%d/', blank=True, null=True, verbose_name='Аватар')
    created_at = models.ImageField(auto_now_add=True, verbose_name='Создан')
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Профиль {self.user.username}'
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile') #Это поле создает связь
    # "один-к-одному" между моделью User и моделью Profile.
    nickname = models.CharField(max_length=50, blank=True, verbose_name='Никнейм')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар') #то поле позволяет
    # пользователям загружать аватар (изображение)

    def __str__(self):
        return f"Профиль {self.user.username}"

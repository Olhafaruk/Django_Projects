from django.contrib.auth import  get_user_model
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.models import EmailAddress

from .models import Profile
from news.models import Category

@receiver(post_save, sender=EmailAddress)
def update_verified_status(sender, instance, **kwargs):
    # Убираем проверку на created, чтобы обрабатывать все случаи
    if instance.verified:
        print(f"[SIGNAL] Email подтвержден: {instance.email}")
        EmailAddress.objects.filter(user=instance.user).exclude(pk=instance.pk).update(verified=True)


@receiver([post_save, post_delete], sender=Category)
def clear_category_cache(sender, **kwargs):
     cache.delete("categories")

#игналы Django для автоматического создания или обновления профиля пользователя, связанного с моделью User
User = get_user_model() #возвращает текущую модель пользователя, определенную в настройках Django (AUTH_USER_MODEL).


@receiver(post_save, sender=User) #связывает функцию с сигналом post_save, который отправляется каждый раз, когда
# объект модели User сохраняется. Аргумент sender=User указывает, что сигнал будет ловить события, связанные именно
# с моделью User
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
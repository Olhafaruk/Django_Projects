from django.contrib.admin import register
from django import template

from ..models import Like


register = template.Library()


@register.filter(name='has_liked')
def has_liked(article, ip_address): #Добавлен новый фильтр `has_liked, проверяет, поставил ли пользователь лайк на статью
    return Like.objects.filter(article=article, ip_address=ip_address).exists()
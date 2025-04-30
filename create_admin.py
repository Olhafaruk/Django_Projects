#!/usr/bin/env python
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itg.settings')


django.setup()  # Сначала вызываем настройку Django, только потом импорты моделей!


from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp


User = get_user_model()


# Параметры суперпользователя
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpass')


# Создание суперпользователя
if not User.objects.filter(username=username).exists():
    print("Creating superuser...")
    User.objects.create_superuser(username=username, email=email, password=password)
else:
    print("Superuser already exists.")


# Настройка Site с ID=1
site, created = Site.objects.get_or_create(id=1, defaults={
    'domain': '127.0.0.1',
    'name': '127.0.0.1'
})

if not created:
    site.domain = '127.0.0.1'
    site.name = '127.0.0.1'
    site.save()
    print("Updated Site id=1 to 127.0.0.1")
else:
    print("Created Site id=1 with 127.0.0.1")


# Создание SocialApp для GitHub
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')

if not SocialApp.objects.filter(provider='github', client_id=client_id).exists():
    print("Creating SocialApp for GitHub...")
    app = SocialApp.objects.create(
        provider='github',
        name='GitHub',
        client_id=client_id,
        secret=client_secret,
    )
    app.sites.add(site)  # привязываем приложение к созданному сайту
    app.save()
else:
    print("SocialApp for GitHub already exists.")
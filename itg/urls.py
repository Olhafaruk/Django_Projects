"""
URL configuration for itg project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from news import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='index'),
    path('about/', views.about, name='about'),
    path('news/', include('news.urls')),
]


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', views.main),
#     path('info/', views.info),
#     path('news/', views.get_all_news),
#     path('news/<int:news_id>/', views.get_news_by_id),
# ]
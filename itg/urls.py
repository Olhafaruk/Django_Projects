from django.contrib import admin
from django.urls import path, include

from itg import settings
from news import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='index'),
    path('about/', views.about, name='about'),
    path('news/', include('news.urls', namespace='news')),
    path('news/', include('news.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
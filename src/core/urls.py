# coding: utf-8
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core.views import index

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')),
    path('admin/', admin.site.urls),
    path('docs/', include('apps.docs.urls')),


    path('', index, name='index')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

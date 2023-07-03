# coding: utf-8
"""Patrones de rutas generales."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core.views import Index, EncuestasIndex


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('docs/', include('apps.docs.urls')),
    path('carto/', include('apps.carto.urls')),
    path('mejora/', include('apps.ideas.urls')),
    path('', Index.as_view(), name='index')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

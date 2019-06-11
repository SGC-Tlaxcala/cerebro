# coding: utf-8
"""Patrones de rutas generales."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core.views import index, EncuestasIndex

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),

    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.jwt')),
    # path('auth/', include('djoser.urls.authtoken')),
    path('admin/', admin.site.urls),
    path('docs/', include('apps.docs.urls')),
    path('mesas/', include('apps.mesas.urls')),
    path('paquetes/', include('apps.paquetes.urls')),
    path('cifras/', include('apps.productividad.urls')),
    path('dpi/', include('apps.dpi.urls')),
    path('cecyrd/', include('apps.cecyrd.urls')),
    path('encuestas/', EncuestasIndex.as_view(), name='encuestas'),
    path('aprobacion/', include('apps.aprobacion.urls')),
    path('cobertura/', include('apps.cobertura.urls')),
    path('incidencias/', include('apps.incidencias.urls')),
    path('', index, name='index')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

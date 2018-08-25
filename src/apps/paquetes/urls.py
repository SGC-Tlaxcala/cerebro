# coding: utf-8
# app: paquetes
# module: URLs
# date: 24 Aug 2018
# author: Javier Sanchez Toledano <js.toledano@me.com>
# description: Patrones de búsqueda

from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from apps.paquetes.views import (
    PaquetesIndex,
    envio_paso1,
    envio_paso2,
    EnvioDistrito,
    envio_expediente,
    PaqueteDetalle,
    envio_ajax_suma_paquete
)

app_name = 'paquetes'
urlpatterns = [
    path('', PaquetesIndex.as_view(), name="index"),
    path('paso1/', login_required(envio_paso1), name='envio_paso1'),
    path('paso2/', login_required(envio_paso2), name='envio_paso2'),
    path('distrito/<int:distrito>', EnvioDistrito.as_view(), name="envio_distrito"),
    re_path(r'^remesa/(?P<remesa>\d{4}-\d{2})/(?P<distrito>\d)/$', PaqueteDetalle.as_view(), name='detalle'),
    re_path(r'^envio/(?P<envio>\d+)$', login_required(envio_expediente), name='envio_expediente'),
    re_path(r'^suma/(?P<envio>\d+)$', envio_ajax_suma_paquete)
]

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
    envio_distrito,
    envio_expediente,
    PaqueteDetalle,
    envio_ajax_suma_paquete
)

app_name = 'paquetes'
urlpatterns = [
    path('', PaquetesIndex.as_view(), name="index"),
    re_path(r'^remesa/(?P<remesa>\d{4}-\d{2})/(?P<distrito>\d)/$', PaqueteDetalle.as_view(), name='detalle'),
    path('paso1/', envio_paso1, name='envio_paso1'),
    path('paso2/', envio_paso2, name='envio_paso2'),
    re_path(r'^envio/(?P<envio>\d+)$', envio_expediente, name='envio_expediente')

]

#     url(r"^$", "distro_index", name="distribucion"),
#     url(r'^envio/(?P<envio>\d+)$', 'envio_expediente', name='envio_expediente'),
#     url(r"^paso1/$", 'envio_paso1', name='envio_paso1'),
#     url(r"^paso2/$", 'envio_paso2', name='envio_paso2'),
#
#     url(r'^distrito/(?P<dist>\d)$', 'envio_distrito', name="envio_distrito"),
#     # url(r'^suma/(?P<envio>\d+)$', 'envio_ajax_suma_paquete'),
#     url(r'^remesa/(?P<remesa>\d{4}\-\d{2})/(?P<distrito>\d)/$', 'envio_remesa', name='envio_remesa')
# )

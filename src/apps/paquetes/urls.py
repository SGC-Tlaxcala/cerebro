# coding: utf-8
# app: paquetes
# module: URLs
# date: 24 Aug 2018
# author: Javier Sanchez Toledano <js.toledano@me.com>
# description: Patrones de búsqueda

from django.urls import path
from django.contrib.auth.decorators import login_required
from apps.paquetes.views import (
    distro_index,
    envio_paso1,
    envio_paso2,
    envio_distrito,
    envio_remesa,
    envio_ajax_suma_paquete
)

app_name = 'paquetes'
urlpatterns = [
    path('', distro_index, name="index"),
    path('paso1/', envio_paso1, name='envio_paso1'),
    path('paso2/', envio_paso2, name='envio_paso2'),

    path('remesa/<str:remesa>/<int:distrito>', envio_remesa, name='envio_remesa')
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

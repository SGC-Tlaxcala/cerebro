# coding: utf-8
# app: productividad
# module: urls
# date: 26 Aug 2018
# author: Javier Sanchez Toledano <js.toledano@me.com>
"""Patrones de URI para productividad"""

from django.urls import path
from django.contrib.auth.decorators import login_required
from apps.productividad.views import (
    CifrasUpload,
    CifrasPortada,
    RemesaDetalle,
    TramitesIndex,
    EntregasIndex
)

app_name = 'cifras'
urlpatterns = [
    path('', CifrasPortada.as_view(), name='index'),
    path('tramites/', TramitesIndex.as_view(), name='tramites'),
    path('entregas/', EntregasIndex.as_view(), name='entregas'),
    path('detalle/<int:pk>/', RemesaDetalle.as_view(), name='detalle'),
    path('add', login_required(CifrasUpload.as_view()), name="add")
]

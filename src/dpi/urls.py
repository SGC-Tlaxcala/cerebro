# coding: utf-8
"""Rutas de DPI."""
#         app: dpi
#      módulo: urls
# descripción: rutas
#       autor: Javier Sanchez Toledano
#       fecha: lunes, 28 de mayo de 2018


from django.urls import path
from dpi.views import DPIIndex

app_name = 'dpi'
urlpatterns = [
    path('', DPIIndex.as_view(), name='index_dpi')
]

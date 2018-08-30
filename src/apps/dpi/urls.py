# coding: utf-8
"""Rutas de DPI."""
#         app: dpi
#      módulo: urls
# descripción: rutas
#       autor: Javier Sanchez Toledano
#       fecha: lunes, 28 de mayo de 2018


from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.dpi.views import DPIAdd, DPIEdit, DPIIndex

app_name = 'dpi'
urlpatterns = [
    path('', DPIIndex.as_view(), name='index'),
    path('add/', login_required(DPIAdd.as_view()), name='dpi_add'),
    path('<str:folio>/edit/', login_required(DPIEdit.as_view()), name='edit')
]

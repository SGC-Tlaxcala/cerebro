# coding: utf-8
u"""Vistas de Depuración."""

#         app: dpi
#      módulo: vies
# descripción: Vistas de DPI y USI
#       autor: Javier Sanchez Toledano
#       fecha: lunes, 28 de mayo de 2018

from django.shortcuts import render
from dpi.forms import ExpedienteForm


def index(request):
    """Vista del index de DPI."""
    form = ExpedienteForm()
    return render(request, 'dpi/index.html', {'form': form})

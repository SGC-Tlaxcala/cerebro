# coding: utf-8
u"""Vistas de Depuración."""

#         app: dpi
#      módulo: vies
# descripción: Vistas de DPI y USI
#       autor: Javier Sanchez Toledano
#       fecha: lunes, 28 de mayo de 2018

from django.shortcuts import render
from django.views.generic import TemplateView

from dpi.forms import ExpedienteForm


class DPIIndex(TemplateView):
  template_name = 'dpi/index.html'
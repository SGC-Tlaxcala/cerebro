# coding: utf-8
# app: apps.productividad.views
# author: Javier Sanchez Toledano <js.toledano@me.com>
# date: 26/08/2018
"""Vista para subir el archivo de la productividad."""

from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views import View
from apps.productividad.forms import CargaCifras


class CifrasUpload(View):
    template_name = 'productividad/index.html'
    form_class = CargaCifras

    def get(self, request, *args, **kwargs):
        contexto = {
            'title': 'Carga de archivo de cifras',
            'kpi_path': True,
            'form': self.form_class()
        }
        return render(request, self.template_name, contexto)

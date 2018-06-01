# coding: utf-8
u"""Vistas de Depuración."""

#         app: dpi
#      módulo: vies
# descripción: Vistas de DPI y USI
#       autor: Javier Sanchez Toledano
#       fecha: lunes, 28 de mayo de 2018

from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from rest_framework import viewsets
from rest_framework.response import Response

from .models import ExpedienteDPI
from .forms import ExpedienteForm
from .serializers import ExpedienteSerializer


class DPIIndex(TemplateView):
    template_name = 'dpi/index.html'


class DPIAdd(FormView):
    template_name = 'dpi/add.html'
    form_class = ExpedienteForm
    success_url = '/dpi/add'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.usuario = self.request.user
        self.object.save()
        messages.success(self.request, f'El registro {self.object.tipo}_{self.object.folio} se guardó correctamente')
        return super().form_valid(form)


class ExpedienteSimpleViewSet(viewsets.ViewSet):
    """Permite determinar si existe un expediente o no."""

    def list(self, request):
        queryset = ExpedienteDPI.objects.all()
        serializer = ExpedienteSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, folio=None):
        queryset = ExpedienteDPI.objects.all()
        expediente = get_object_or_404(queryset, folio=folio)
        serializer = ExpedienteSerializer(expediente)
        return Response(serializer.data)

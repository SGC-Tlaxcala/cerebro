# coding: utf-8
u"""Vistas de Depuración."""

#         app: dpi
#      módulo: vies
# descripción: Vistas de DPI y USI
#       autor: Javier Sanchez Toledano
#       fecha: lunes, 28 de mayo de 2018

from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from rest_framework import viewsets
from rest_framework.response import Response

from dpi.models import ExpedienteDPI
from dpi.serializers import ExpedienteSerializer


class DPIIndex(TemplateView):
    template_name = 'dpi/index.html'


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

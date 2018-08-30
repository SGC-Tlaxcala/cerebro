# coding: utf-8
"""Vistas de Depuración."""

#         app: dpi
#      módulo: vies
# descripción: Vistas de DPI y USI
#       autor: Javier Sanchez Toledano
#       fecha: lunes, 28 de mayo de 2018

from django.contrib import messages
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.dpi.forms import ExpedienteForm
from apps.dpi.models import ExpedienteDPI
from apps.dpi.serializers import ExpedienteSerializer


def porciento(completo, total):
    """Evita el error de la división por cero"""
    try:
        return (completo / total) * 100
    except ZeroDivisionError:
        return 0


class DPIIndex(View):
    """Portada de DPI"""
    template_name = 'dpi/index.html'
    year = 2018

    def get(self, request, *args, **kwargs):
        """Verbo GET de la vista"""

        year = self.year
        fecha = Q(fecha_tramite__year=year)
        dpi = Q(tipo='DPI')
        tlaxcala = Q(entidad=29)
        completo = Q(completo=1)

        tlx = ExpedienteDPI.objects.filter(tlaxcala, fecha, dpi).prefetch_related()

        delta = tlx.values('distrito').order_by('distrito').annotate(atencion=Avg('delta_distrito'))

        estatal = {
            'total': tlx.count(),
            'completos': tlx.filter(completo).count(),
            'incompletos': tlx.count()- tlx.filter(completo).count(),
            'porcentaje': porciento(tlx.filter(completo).count(), tlx.count()),
            'delta': delta
        }

        _distritos = {}

        for distrito in (1, 2, 3):
            _total = tlx.filter(distrito=distrito).order_by('folio')
            _completos = _total.filter(completo).count()
            _incompletos = _total.count() - _completos
            _distritos[distrito] = {
                'total': _total.count(),
                'completos': _completos,
                'incompletos': _incompletos,
                'porcentaje': porciento(_completos, _total.count()),
                'registros': _total
            }

        data = {
            'year': year,
            'title': 'Control de DPI',
            'estatal': estatal,
            'distritos': (1, 2, 3),
            'distrito': _distritos,
            'kpi_path': True
        }
        return render(request, self.template_name, data)


class DPIAdd(CreateView):
    """Registro de nueva cédula"""
    model = ExpedienteDPI
    template_name = 'dpi/add.html'
    form_class = ExpedienteForm
    success_url = reverse_lazy('dpi:dpi_add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'kpi_path': True})
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False) # pylint: disable=W0201
        self.object.usuario = self.request.user
        self.object.save()
        messages.success(
            self.request,
            f'El registro {self.object.tipo}_{self.object.folio} \
            <strong>se guardó</strong> correctamente'
        )
        return super().form_valid(form)


class DPIEdit(UpdateView):
    """Edición de cédulas"""
    model = ExpedienteDPI
    template_name = 'dpi/add.html'
    form_class = ExpedienteForm
    success_url = reverse_lazy('dpi:dpi_add')

    def get_object(self, queryset=None):
        return get_object_or_404(ExpedienteDPI, folio=self.kwargs['folio'])

    def form_valid(self, form):
        self.object = form.save(commit=False) # pylint: disable=W0201
        self.object.usuario = self.request.user
        self.object.save()
        messages.success(
            self.request,
            f'El registro {self.object.tipo}_{self.object.folio} se \
            <strong>editó</strong> correctamente'
        )
        return super().form_valid(form)


class ExpedienteSimpleViewSet(viewsets.ViewSet):
    """Permite determinar si existe un expediente o no."""

    def list(self, request):
        """Muestra la lista de expedientes"""
        queryset = ExpedienteDPI.objects.all()
        serializer = ExpedienteSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, folio=None):
        """Recupera la lista de expedientes"""
        queryset = ExpedienteDPI.objects.all()
        expediente = get_object_or_404(queryset, folio=folio)
        serializer = ExpedienteSerializer(expediente)
        return Response(serializer.data)


class ExpedienteIncompletoViewSet(viewsets.ReadOnlyModelViewSet):
    """Busca expedientes incompletos"""
    queryset = ExpedienteDPI.objects.filter(Q(completo=1), Q(entidad=29))
    serializer_class = ExpedienteSerializer
    permission_classes = [AllowAny, ]

# coding: utf-8
u"""Vistas de Depuración."""

#         app: dpi
#      módulo: vies
# descripción: Vistas de DPI y USI
#       autor: Javier Sanchez Toledano
#       fecha: lunes, 28 de mayo de 2018

from django.contrib import messages
from django.db.models import Q, F
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView

from rest_framework import viewsets
from rest_framework.response import Response

from dpi.models import ExpedienteDPI
from dpi.forms import ExpedienteForm
from dpi.serializers import ExpedienteSerializer

DPI = Q(tipo='DPI')
USI = Q(tipo='USI')
TLAXCALA = Q(entidad=29)


class ExpedientesIncompletos(ListView):
    model = ExpedienteDPI
    context_object_name = 'expedientes'
    paginate_by = 6
    make_object_list = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'kpi_path': True})
        return context


class DPIIndex(TemplateView):
    template_name = 'dpi/index.html'
    YEAR = 2017
    total = ExpedienteDPI.objects.all()
    total_dpi = total.filter(DPI)
    total_usi = total.filter(USI)

    tlaxcala_total = ExpedienteDPI.objects.filter(TLAXCALA)
    tlaxcala_total_dpi = tlaxcala_total.filter(DPI)
    tlaxcala_total_usi = tlaxcala_total.filter(USI)

    hay_tramite = Q(fecha_tramite__isnull=False)
    hay_notificacion = Q(fecha_notificacion_aclaracion__isnull=False)
    hay_fecha_entrevista = Q(fecha_entrevista__isnull=False)
    hay_fecha_envio_expediente = Q(fecha_envio_expediente__isnull=False)

    tlx_dpi_exp_completo = tlaxcala_total_dpi.filter(
        hay_tramite,
        hay_notificacion,
        hay_fecha_entrevista,
        hay_fecha_envio_expediente
    )

    contexto = {
        'year': YEAR
        , 'total_count': total.count()
        , 'total_dpi': total_dpi.count()
        , 'total_usi': total_usi.count()

        , 'tlaxcala_count': tlaxcala_total.count()
        , 'tlaxcala_total_dpi': tlaxcala_total_dpi.count()
        , 'tlaxcala_total_usi': tlaxcala_total_usi.count()

        , 'tlx_dpi_exp_completo': tlx_dpi_exp_completo.count()
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'kpi_path': True})
        context.update(self.contexto)
        return context


class DPIAdd(CreateView):
    model = ExpedienteDPI
    template_name = 'dpi/add.html'
    form_class = ExpedienteForm
    success_url = reverse_lazy('dpi:dpi_add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'kpi_path': True})
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.usuario = self.request.user
        self.object.save()
        messages.success(
            self.request,
            f'El registro {self.object.tipo}_{self.object.folio} <strong>se guardó</strong> correctamente'
        )
        return super().form_valid(form)


class DPIEdit(UpdateView):
    model = ExpedienteDPI
    template_name = 'dpi/add.html'
    form_class = ExpedienteForm
    success_url = reverse_lazy('dpi:dpi_add')

    def get_object(self):
        return get_object_or_404(ExpedienteDPI, folio=self.kwargs['folio'])

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.usuario = self.request.user
        self.object.save()
        messages.success(
            self.request,
            f'El registro {self.object.tipo}_{self.object.folio} se <strong>editó</strong> correctamente'
        )
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

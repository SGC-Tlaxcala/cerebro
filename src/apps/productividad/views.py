# coding: utf-8
# app: apps.productividad.views
# author: Javier Sanchez Toledano <js.toledano@me.com>
# date: 26/08/2018
"""Vista para subir el archivo de la productividad."""

import math
import xlrd
from datetime import datetime

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Sum, F
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from apps.productividad.forms import CargaCifras
from apps.productividad.models import Cifras, PronosticoTramites, Reporte
from core.utils import Remesa

scope = F('fecha_corte__year=2020')
YEAR = 2020
YEARS = (2019, 2020)
CAP = '2019-12-16'
CAI = '2020-08-31'


def get_int(celda):
    """Convierte el valor de una celda en entero"""
    if celda.value == '':
        return 0
    try:
        if celda.ctype != 2:
            return 0
        return math.ceil(celda.value)
    except ValueError:
        return 0


def get_float(celda):
    """"Convierte el valor de una celda en un número flotante"""
    # valor = 0
    try:
        valor = float(celda.value)
    except ValueError:
        valor = 0
    return valor


def procesar_cifras(archivo_excel):
    """Procesa el archivo de cifras"""
    try:
        cifras = xlrd.open_workbook(archivo_excel).sheet_by_name("CIFRAS_PRODUCCION DIARIA")
    except xlrd.XLRDError:
        cifras = xlrd.open_workbook(archivo_excel).sheet_by_name("CIFRAS_PRODUCCION SEMANAL")
    remesa = list(filter(None, cifras.row_values(6)))[0][8:].replace('_', '-')
    if cifras.cell(31, 0).value.find('Observaciones') > 0:
        observaciones = cifras.cell(32, 0).value
    else:
        observaciones = cifras.cell(33, 0).value
    macs = {}

    for row in range(8, 30):
        mac = cifras.row(row)
        size = len(mac)
        try:
            modulo = str(int(mac[0].value))
            if modulo[:3] == '290':
                macs[modulo] = {
                    'distrito': modulo[2:4],
                    'tipo': mac[1].value,
                    'dias_trabajados': get_int(mac[2]),
                    'jornada_trabajada': get_float(mac[3]),
                    'configuracion': mac[4].value,
                    'tramites': get_int(mac[5]),
                    'credenciales_entregadas_actualizacion': get_int(mac[6]),
                    'credenciales_reimpresion': get_int(mac[7]) if size == 13 else 0,
                    'total_atenciones': get_int(mac[8]) if size == 13 else get_int(mac[7]),
                    'productividad_x_dia': get_int(mac[9]) if size == 13 else get_int(mac[8]),
                    'productividad_x_dia_x_estacion': get_int(mac[10]) if size == 13 else get_int(mac[9]),
                    'credenciales_recibidas': get_int(mac[12]) if size == 13 else get_int(mac[11])
                }
        except ValueError:
            pass

    return observaciones, remesa, macs


class CifrasPortada(ListView):
    """Para crear la portada"""
    model = Reporte
    template_name = 'productividad/index.html'
    context_object_name = 'reportes'

    def __init__(self):
        super().__init__()
        self.year = YEAR

    def dispatch(self, request, *args, **kwargs):
        self.year = self.request.GET.get("year", YEAR)
        return super(CifrasPortada, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        return Reporte.objects.filter(fecha_corte__gte=CAP, fecha_corte__lte=CAI).order_by('fecha_corte')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = int(self.year)
        context['years'] = YEARS
        context['title'] = f"Productividad {self.year}"
        context['current_year'] = int(datetime.now().year)
        context['same_year'] = int(self.year) == int(datetime.now().year)
        context['kpi_path'] = True
        context['periodo'] = {
            'inicio': self.get_queryset().first(),
            'fin': self.get_queryset().last()
        }
        return context


class RemesaDetalle(DetailView):
    """Clase para visualizar el informe de productividad"""
    model = Reporte
    template_name = 'productividad/remesa_detalle.html'
    context_object_name = 'reporte'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rem'] = Remesa.objects.get(remesa=self.object.remesa[:7])
        context['title'] = 'Reporte de productividad en los módulos de atención ciudadana'
        context['kpi_path'] = True
        return context


class CifrasUpload(FormView):
    """Con esta clase subo el archivo"""
    form_class = CargaCifras
    template_name = 'productividad/add.html'
    reporte = 1

    def form_valid(self, form):
        fecha = form.cleaned_data['fecha_corte']
        archivo = self.get_form_kwargs().get('files')['archivo']
        path = default_storage.save(
            settings.MEDIA_ROOT.child('productividad', f"remesa-{fecha.strftime('%Y%m%d')}.xls"),
            ContentFile(archivo.read())
        )
        (observaciones, remesa, macs) = procesar_cifras(path)
        self.reporte, created = Reporte.objects.update_or_create(
            remesa=remesa,
            defaults={
                'fecha_corte': fecha,
                'remesa': remesa,
                'notas': observaciones,
                'archivo': path,
                'usuario': self.request.user
            }
        )
        reporte_actividad = 'creó' if {created} else 'actualizó'
        print(f"cerebro:: El reporte {self.reporte} se {reporte_actividad}")
        for mac in macs:
            cifras, created = Cifras.objects.update_or_create(
                reporte_semanal=self.reporte, modulo=mac,
                defaults={
                    'reporte_semanal': self.reporte,
                    'distrito': macs[mac]['distrito'],
                    'modulo': mac,
                    'tipo': macs[mac]['tipo'],
                    'dias_trabajados': macs[mac]['dias_trabajados'],
                    'jornada_trabajada': macs[mac]['jornada_trabajada'],
                    'configuracion': macs[mac]['configuracion'],
                    'tramites': macs[mac]['tramites'],
                    'credenciales_entregadas_actualizacion':
                        macs[mac]['credenciales_entregadas_actualizacion'],
                    'credenciales_reimpresion': macs[mac]['credenciales_reimpresion'],
                    'total_atenciones': macs[mac]['total_atenciones'],
                    'productividad_x_dia': macs[mac]['productividad_x_dia'],
                    'productividad_x_dia_x_estacion': macs[mac]['productividad_x_dia_x_estacion'],
                    'credenciales_recibidas': macs[mac]['credenciales_recibidas']
                }
            )
            actividad = 'crearon' if {created} else 'actualizaron'
            print(f'cerebro:: Se {actividad} los datos {mac} en el registro {cifras}')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('cifras:detalle', kwargs={'pk': self.reporte.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Carga de archivo de cifras'
        context['kpi_path'] = True
        return context


class Productividad(View):
    def __init__(self):
        super(View, self).__init__()
        self.year = YEAR
        self.years = YEARS
        self.tramites = None
        self.entregas = None
        self.periodo = {}
        self.current_year = int(datetime.now().year)

    def dispatch(self, request, *args, **kwargs):
        self.year = self.request.GET.get("year", YEAR)
        self.tramites = Cifras.objects\
            .filter(reporte_semanal__fecha_corte__year=self.year)\
            .values('distrito')\
            .order_by('distrito')\
            .annotate(suma_modulo=Sum('tramites'))
        self.entregas = Cifras.objects.values('distrito')\
            .filter(reporte_semanal__fecha_corte__year=self.year)\
            .order_by('distrito')\
            .annotate(entregas_distrito=Sum('credenciales_entregadas_actualizacion'))
        self.periodo = {
            'inicio': Reporte.objects.filter(fecha_corte__year=self.year).order_by('fecha_corte').first(),
            'fin': Reporte.objects.filter(fecha_corte__year=self.year).order_by('fecha_corte').last()
        }
        return super(Productividad, self).dispatch(request, *args, **kwargs)


class TramitesIndex(Productividad):
    """Vista para indicador de trámites"""
    template_name = 'productividad/tramites.html'

    def get(self, request):
        """Control para el verbo GET"""

        pronostico = PronosticoTramites.objects.all().filter().filter(year=self.year)
        chart_data = []

        for _distrito in ('01', '02', '03'):
            dlist = [_distrito]
            _tramites = 0
            _pronostico = 0
            for _cifras in self.tramites:
                if _cifras['distrito'] == _distrito:
                    _tramites = _cifras['suma_modulo']
                    dlist.append(_tramites)
            for _pt in pronostico:
                if f'0{_pt.distrito}' == _distrito:
                    _pronostico = _pt.tramites
                    dlist.append(_pronostico)
            dlist.append(_pronostico - _tramites)
            dlist.append((_tramites / _pronostico) * 100)
            chart_data.append(dlist)

        estatal = {
            'tramites': sum(r[1] for r in chart_data),
            'faltantes': sum(r[2] for r in chart_data) - sum(r[1] for r in chart_data),
            'pronostico': sum(r[2] for r in chart_data),
            'porcentaje': (sum(r[1] for r in chart_data) / sum(r[2] for r in chart_data)) * 100
        }

        data = {
            'chart_data': chart_data,
            'years': self.years,
            'year': int(self.year),
            'current_year': self.current_year,
            'same_year': int(self.year) == int(datetime.now().year),
            'estatal': estatal,
            'kpi_path': True,
            'title': f'Control de Trámites {self.year}',
            'periodo': self.periodo
        }

        return render(request, self.template_name, data)


class EntregasIndex(Productividad):
    """Visualización de cobertura"""
    template_name = 'productividad/entregas.html'

    def get(self, request):
        """verbo get de entregas"""
        _data_entregas = {'01': {}, '02': {}, '03': {}}
        for _distrito in _data_entregas.keys():
            for row in self.entregas:
                if row['distrito'] == _distrito:
                    _data_entregas[_distrito]['entregas'] = row['entregas_distrito']
            for row in self.tramites:
                if row['distrito'] == _distrito:
                    _data_entregas[_distrito]['tramites'] = row['suma_modulo']
            _data_entregas[_distrito]['relacion'] =\
                (
                    _data_entregas[_distrito]['entregas'] / _data_entregas[_distrito]['tramites']
                ) * 100
            _data_entregas[_distrito]['diferencia'] = (
                    _data_entregas[_distrito]['tramites'] - _data_entregas[_distrito]['entregas']
            )
        entregas_estatal = 0
        tramites_estatal = 0
        for k, values in _data_entregas.items():
            entregas_estatal += _data_entregas[k]['entregas']
            tramites_estatal += _data_entregas[k]['tramites']
        relacion_estatal = (entregas_estatal / tramites_estatal) * 100
        diferencia_estatal = tramites_estatal - entregas_estatal
        estatal = {
            'entregas': entregas_estatal,
            'tramites': tramites_estatal,
            'diferencia': diferencia_estatal,
            'relacion': relacion_estatal
        }
        data = {
            'title': f'Control de Entregas {self.year}',
            'years': self.years,
            'year': int(self.year),
            'current_year': self.current_year,
            'same_year': int(self.year) == int(datetime.now().year),
            'distritos': _data_entregas,
            'estatal': estatal,
            'kpi_path': True,
            'periodo': self.periodo
        }
        return render(request, self.template_name, data)

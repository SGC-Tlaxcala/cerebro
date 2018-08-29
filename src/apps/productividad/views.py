# coding: utf-8
# app: apps.productividad.views
# author: Javier Sanchez Toledano <js.toledano@me.com>
# date: 26/08/2018
"""Vista para subir el archivo de la productividad."""

import math
import xlrd
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import Sum
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.urls import reverse
from core.utils import Remesa
from apps.productividad.forms import CargaCifras
from apps.productividad.models import Reporte, Cifras, PronosticoTramites


TRAMITES = Cifras.objects.values('distrito')\
    .order_by('distrito')\
    .annotate(suma_modulo=Sum('tramites'))

ENTREGAS = Cifras.objects.values('distrito')\
            .order_by('distrito')\
            .annotate(entregas_distrito=Sum('credenciales_entregadas_actualizacion'))


def get_int(celda):
    """Convierte el valor de una celda en entero"""
    try:
        if celda.ctype == 5:
            return 0
        return math.ceil(celda.value)
    except ValueError:
        return 0


def procesar_cifras(archivo_excel):
    """Procesa el archivo de cifras"""
    cifras = xlrd.open_workbook(archivo_excel).sheet_by_name("CIFRAS_PRODUCCION DIARIA")
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
                    'jornada_trabajada': mac[3].value,
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

        if '290260' not in macs:
            macs['290260'] = {
                'distrito': '02',
                'tipo': 'Urbano',
                'dias_trabajados': 0,
                'jornada_trabajada': 0,
                'configuracion': 'B',
                'tramites': 0,
                'credenciales_entregadas_actualizacion': 0,
                'credenciales_reimpresion': 0,
                'total_atenciones': 0,
                'productividad_x_dia': 0,
                'productividad_x_dia_x_estacion': 0,
                'credenciales_recibidas': 0
            }

    return observaciones, remesa, macs


class CifrasPortada(ListView):
    """Para crear la portada"""
    model = Reporte
    template_name = 'productividad/index.html'
    context_object_name = 'reportes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Productividad"
        context['kpi_path'] = True
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


class TramitesIndex(View):
    """Vista para indicador de trámites"""
    template_name = 'productividad/tramites.html'

    def get(self, request, *args, **kwargs):
        """Control para el verbo GET"""

        pronostico = PronosticoTramites.objects.all()

        chart_data = [
        ]

        for _distrito in ('01', '02', '03'):
            dlist = [_distrito]
            _tramites = 0
            _pronostico = 0
            for _cifras in TRAMITES:
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
            'porcentaje': (sum(r[1] for r in chart_data)/ sum(r[2] for r in chart_data)) * 100
        }

        data = {
            'chart_data': chart_data,
            'estatal': estatal,
            'kpi_path': True,
            'title': 'Control de Trámites'
        }

        return render(request, self.template_name, data)


class EntregasIndex(View):
    """Visualización de cobertura"""
    template_name = 'productividad/entregas.html'

    def get(self, request, *args, **kwargs):
        """verbo get de entregas"""
        _data_entregas = {'01': {}, '02': {}, '03': {}}
        for _distrito in _data_entregas.keys():
            for row in ENTREGAS:
                if row['distrito'] == _distrito:
                    _data_entregas[_distrito]['entregas'] = row['entregas_distrito']
            for row in TRAMITES:
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
            'title': 'Control de Entregas',
            'distritos': _data_entregas,
            'estatal': estatal,
            'kpi_path': True,
        }
        return render(request, self.template_name, data)

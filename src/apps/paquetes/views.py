# coding: utf-8
# app: paquetes
# module: views
# date: 24 Aug 2018
# author: Javier Sanchez Toledano <js.toledano@me.com>
# description: Vistas de la distribución de paquetes

from collections import OrderedDict
from django.shortcuts import render_to_response
from django.db.models import Avg, Sum, Q, Max
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from core.models import Modulo, Remesa
from core.utils import get_remesa
from .models import Envio, EnvioModulo
from .forms import PrepareForm, EnvioModuloForm

YEAR = 2018


# Expediente de envio
def envio_expediente(request, envio):
    e = Envio.objects.get(pk=envio)
    tran_tmp = e.recibido_vrd - e.envio_cnd
    transito = (tran_tmp.seconds / 60)
    return render(
        request, "paquetes/envio_expediente.html", {
            'e': e, 'transito': transito,
            'title': 'Expediente del Envío'
        }
    )


class EnvioDistrito(View):
    template_name = 'paquetes/distrito.html'

    # noinspection PyUnusedLocal
    def get(self, request, *args, **kwargs):
        macs = Modulo.objects.filter(distrito=kwargs['distrito'])
        return render(request, self.template_name, {'macs': macs, 'kpi_path': True})


def envio_ajax_suma_paquete(request, envio):
    e = Envio.objects.get(pk=envio)
    suma = e.enviomodulo_set.aggregate(Sum('formatos'))
    return render_to_response(
        "paquetes/envio_ajax_suma_paquete.html",
        {'suma': suma['formatos__sum']},
    )


class PaquetesIndex(View):
    template_name = 'paquetes/index.html'

    # noinspection PyUnusedLocal
    def get(self, request, *args, **kwargs):
        tramo_local = OrderedDict()
        tabla_local = OrderedDict()
        tramo_cnd = OrderedDict()

        envio_modulo = EnvioModulo.objects.values('lote__fecha_corte', 'lote__distrito')\
            .annotate(Avg('tran_sec'), Max('lote__recibido_vrd'))\
            .order_by('lote__fecha_corte', 'lote__distrito')\
            .filter(lote__fecha_corte__year=YEAR)\
            .prefetch_related()
        envio_cnd = Envio.objects.values('fecha_corte', 'distrito')\
            .annotate(Avg('tran_sec'))\
            .order_by('fecha_corte', 'distrito')\
            .filter(fecha_corte__year=YEAR)\
            .prefetch_related()

        periodo = {
            'inicio': envio_modulo.first(),
            'fin': envio_modulo.last()
        }

        for t in envio_modulo:
            fecha_vrd = t['lote__recibido_vrd__max']
            horas_local = t['tran_sec__avg']
            tramo_local\
                .setdefault(t['lote__fecha_corte'], {})\
                .update({t['lote__distrito']: horas_local, 'vrd': fecha_vrd})
        for t in envio_modulo.order_by('-lote__fecha_corte'):
            fecha_vrd = t['lote__recibido_vrd__max']
            horas_local = t['tran_sec__avg']
            tabla_local\
                .setdefault(t['lote__fecha_corte'], {})\
                .update({t['lote__distrito']: horas_local, 'vrd': fecha_vrd})
        for t in envio_cnd:
            horas = t['tran_sec__avg']
            tramo_cnd\
                .setdefault(t['fecha_corte'], {})\
                .update({t['distrito']: horas})
        mini_parcel = Envio.objects.filter(credenciales__lte=5)

        contexto = {
            'title': 'Distribución de FCPVF',
            'mnDistro': True, 'mnIndicadores': True,
            'tramo_cnd': tramo_cnd,
            'tramo_local': tramo_local,
            'tabla_local': tabla_local,
            'mini_envio': mini_parcel,
            'periodo': periodo,
            'kpi_path': True
        }

        return render(request, self.template_name, contexto)


class PaqueteDetalle(View):
    template_name = 'paquetes/detalle.html'

    # noinspection PyUnusedLocal
    def get(self, request, *args, **kwargs):
        distrito = kwargs['distrito']
        r = Remesa.objects.get(remesa=kwargs['remesa'])
        e = Envio.objects\
            .filter(Q(fecha_corte__gte=r.inicio), Q(fecha_corte__lte=r.fin), distrito=distrito)\
            .prefetch_related()
        emac = EnvioModulo.objects\
            .filter(Q(lote__fecha_corte__gte=r.inicio), Q(lote__fecha_corte__lte=r.fin), lote__distrito=distrito)\
            .prefetch_related()
        contexto = {
            'title': 'Envíos por Distrito y Remesa', 'kpi_path': True,
            'r': r, 'e': e, 'd': distrito, 'emac': emac}
        return render(request, self.template_name, contexto)


FORMS = [
    ('paso1', PrepareForm),
    ('paso2', EnvioModuloForm)
]
TEMPLATES = {
    '0': 'paquetes/envio_paso1.html',
    '1': 'paquetes/envio_paso2.html'
}


@login_required
def envio_paso1(request):
    if request.method == 'POST':
        contexto = request.POST.copy()
        form = PrepareForm(contexto)

        if form.is_valid():
            datos = form.cleaned_data
            try:
                envio = Envio.objects.get(
                    lote=datos['lote'], distrito=datos['distrito'],
                    recibido_vrd=datos['recibido_vrd']
                )
            except Envio.DoesNotExist:
                envio = False

            if envio:
                request.session["env"] = True
                request.session['envio_id'] = envio.id
                request.session['envio_macs'] = request.POST['mac']
                request.session['lote'] = request.POST['lote']
                request.session['envio_distrito'] = request.POST['distrito']

            rem = get_remesa(datos['recibido_vrd'].date())
            obj = form.save(commit=False)
            obj.fecha_corte = rem.fin
            obj.modulos = len(datos['mac'])
            obj.autor = auth.get_user(request)
            obj.transito = obj.recibido_vrd - obj.envio_cnd
            obj.tran_sec = obj.transito.total_seconds()
            obj.save()
            request.session['envio_fecha_corte'] = obj.fecha_corte.isoformat()
            request.session['envio_id'] = obj.id
            request.session['envio_macs'] = datos['mac']
            request.session['envio_distrito'] = datos['distrito']
            return HttpResponseRedirect('/paquetes/paso2/')
    else:
        try:
            del request.session['envio_fecha_corte']
            del request.session['envio_macs']
            del request.session['envio_distrito']
        except KeyError:
            pass
        form = PrepareForm()
    return render(
        request,
        'paquetes/envio_paso1.html',
        {
            'form': form,
            'title': 'Captura de Envio de FCPVF',
            'mnIndicadores': True,
            'mnDistro': True,
            'kpi_path': True
        }
    )


# noinspection PyUnusedLocal
def envio_paso2(request):
    paquetes_form_set = formset_factory(EnvioModuloForm, extra=0)
    try:
        envio = Envio.objects.get(pk=request.session['envio_id'])
    except Envio.DoesNotExist:
        envio = ''
    if request.method == "POST":
        formset = paquetes_form_set(request.POST)
        if formset.is_valid():
            lote = ''
            for form in formset:
                f = form.save(commit=False)
                lote = f.lote
                f.save()
            return redirect(reverse('paquetes:envio_expediente', kwargs={'envio': request.session['envio_id']}))
    else:
        if request.session['envio_fecha_corte'] and request.session['envio_macs'] and request.session['envio_distrito']:
            macs = []
            for m in request.session['envio_macs']:
                macs.append({'mac': m, 'lote': request.session['envio_id']})
            formset = paquetes_form_set(initial=macs)
        else:
            return HttpResponse(request.session['envio_fecha_corte'])
    return render(
        request,
        'paquetes/envio_paso2.html',
        {
            'formset': formset,
            'envio': envio,
            'title': 'Captura de Distribución de Envíos',
            'kpi_path': True
        }
    )

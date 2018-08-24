# coding: utf-8
# app: paquetes
# module: views
# date: 24 Aug 2018
# author: Javier Sanchez Toledano <js.toledano@me.com>
# description: Vistas de la distribución de paquetes

# -*- coding: utf-8 -*-
#        app: cmi.distribucion
#       desc: Vistas de la apps de distribucion de FCPVF

# Modelo y formulario
from .models import Envio, EnvioModulo
from .forms import PreparacionForm, EnvioModuloForm
from django.db.models import Avg, Sum, Q, Max
from collections import OrderedDict
from core.models import Modulo, Remesa
from core.util import remesa
from django.shortcuts import render_to_response
from django.template import RequestContext
from annoying.decorators import render_to
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect, HttpResponse
import logging
logr = logging.getLogger(__name__)


YEAR = 2018

# Expediente de envio
def envio_expediente(request, envio):
    e = Envio.objects.get(pk=envio)
    tran_tmp = e.recibido_vrd - e.envio_cnd
    transito = (tran_tmp.seconds / 60)
    return render_to_response("2014/distribucion/envio_expediente.html",
        {'e':e,
        'transito': transito,
        'title': 'Expendiente del Envío'},
        context_instance=RequestContext(request)
        )

# Vista AJAX auxiliar para generar Módulos
@render_to('2014/distribucion/distrito.html')
def envio_distrito (request, dist):
    mac = Modulo.objects.filter(dto=dist)
    return {'mac':mac}

def envio_ajax_suma_paquete (request, envio):
    e = Envio.objects.get(pk=envio)
    suma = e.enviomodulo_set.aggregate(Sum('formatos'))
    return render_to_response("distribucion/envio_ajax_suma_paquete.html",
    {'suma':suma['formatos__sum']},
    context_instance=RequestContext(request) )


@render_to('2014/distribucion/distro_index.html')
def distro_index (request):
    tramo_local = OrderedDict()
    tabla_local = OrderedDict()
    tramo_cnd   = OrderedDict()

    envio_modulo = EnvioModulo.objects.values('lote__fecha_corte', 'lote__distrito').annotate(Avg('tran_sec'), Max('lote__recibido_vrd')).order_by('lote__fecha_corte', 'lote__distrito').filter(lote__fecha_corte__year=YEAR)
    envio_cnd    = Envio.objects.values('fecha_corte', 'distrito').annotate(Avg('tran_sec')).order_by('fecha_corte', 'distrito').filter(fecha_corte__year=YEAR)

    for t in envio_modulo:
        fecha_vrd   =t['lote__recibido_vrd__max'] # }
        horas_local = t['tran_sec__avg']
        tramo_local.setdefault(t['lote__fecha_corte'], {}).update({t['lote__distrito']:horas_local, 'vrd':fecha_vrd} )
    for t in envio_modulo.order_by('-lote__fecha_corte'):
        fecha_vrd   =t['lote__recibido_vrd__max'] # }
        horas_local = t['tran_sec__avg']
        tabla_local.setdefault(t['lote__fecha_corte'], {}).update({t['lote__distrito']:horas_local, 'vrd':fecha_vrd} )
    for t in envio_cnd:
        horas = t['tran_sec__avg']
        tramo_cnd.setdefault(t['fecha_corte'], {}).update({t['distrito']:horas})
    mini_envios = Envio.objects.filter(credenciales__lte=5)

    return {'title':'Distribución de FCPVF', 'mnDistro':True, 'mnIndicadores':True,
            'tramo_cnd': tramo_cnd, 'tramo_local':tramo_local, 'tabla_local':tabla_local, 'mini_envio':mini_envios}

@render_to('2014/distribucion/envio_remesa.html')
def envio_remesa(request, remesa, distrito):
    r = Remesa.objects.get(remesa=remesa)
    e = Envio.objects.filter(Q(fecha_corte__gte=r.inicio), Q(fecha_corte__lte=r.fin), distrito=distrito)
    emac =  EnvioModulo.objects.filter(Q(lote__fecha_corte__gte=r.inicio), Q(lote__fecha_corte__lte=r.fin), lote__distrito=distrito)
    return {'title':'Envios por Distrito y Remesa', 'r':r, 'e':e, 'd':distrito, 'emac':emac}


FORMS = [
    ('paso1', PreparacionForm),
    ('paso2', EnvioModuloForm)
]
TEMPLATES = {
    '0':'2014/distribucion/envio_paso1.html',
    '1':'2014/distribucion/envio_paso2.html'
}

# ################### #
# ### envio_paso1 ### #
# ################### #
@render_to('2014/distribucion/envio_paso1.html')
@login_required
def envio_paso1(request):
    if request.method == 'POST':
        contexto = request.POST.copy()
        form = PreparacionForm(contexto)
        try:
            envio = Envio.objects.get(lote=request.POST['lote'], distrito=request.POST['distrito'])
        except:
            envio = False
        if envio:
            request.session["env"] = True
            request.session['envio_id'] = envio.id
            request.session['envio_macs'] = request.POST['mac']
            request.session['lote'] = request.POST['lote']
            request.session['envio_distrito'] = request.POST['distrito']
        if form.is_valid():
            datos = form.cleaned_data
            rem = remesa(datos['recibido_vrd'].date())
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
            return HttpResponseRedirect ('/distribucion/paso2/')
    else:
        try:
            del request.session['envio_fecha_corte']
            del request.session['envio_macs']
            del request.session['envio_distrito']
            # request.session.flush()
        except:
            pass
        form = PreparacionForm()
    return {'form': form, 'title':'Captura de Envio de FCPVF',
            'mnIndicadores':True, 'mnDistro':True
    }


# ################### #
# ### envio_paso2 ### #
# ################### #
@login_required
def envio_paso2(request):
    DistribucionFormSet = formset_factory (EnvioModuloForm, extra=0)
    try:
        envio = Envio.objects.get(pk=request.session['envio_id'])
    except:
        envio=''
    if request.method == "POST":
        formset = DistribucionFormSet(request.POST)
        if formset.is_valid():
            lote = '' # pylint disable:
            for form in formset:
                f = form.save(commit=False)
                lote = f.lote
                f.save()
            return HttpResponseRedirect('/distribucion/envio/%s' % request.session['envio_id'])
    else:
        if (request.session['envio_fecha_corte'] and request.session['envio_macs'] and request.session['envio_distrito']):
            # macs_old = Modulo.objects.filter(dto=request.session['envio_distrito']).values('mac')
            macs = []
            for m in request.session['envio_macs'] :
                macs.append({'mac':m, 'lote':request.session['envio_id']})
            formset = DistribucionFormSet(initial=macs)
        else:
            return HttpResponse (request.session['envio_fecha_corte'])
    return render_to_response('2014/distribucion/envio_paso2.html',
        { 'formset': formset,
            'envio':envio,
          'title':'Captura de Distribución de Envios', },
        context_instance = RequestContext(request), )

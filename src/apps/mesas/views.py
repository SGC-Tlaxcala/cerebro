# coding: utf-8
#         app: mesa de atención
#      module: vistas
#        date: jueves, 14 de junio de 2018 - 09:06
# description: Vistas para la app de mesas de atención
# pylint: disable=W0613,R0201,R0903

from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.db.models import Count, Q
from apps.mesas.models import Registro, CAUSAS, ACTA, IDENTIFICACION, COMPROBANTE, INFORMACION, ENTREGA, FICHA, EDAD, HUELLA, OTRO
from apps.mesas.forms import MesaForm


SIN_RECHAZO = Q(causa__in=[INFORMACION, ENTREGA, OTRO])
CON_RECHAZO = ~SIN_RECHAZO
YEAR = 2019


class MesasIndex(TemplateView):
    template_name = 'mesas/index.html'

    base = Registro.objects.filter(fecha__year=YEAR).order_by('-fecha')
    sexo = base.values('sexo').annotate(total=Count('sexo'))
    causas = base.values('causa').annotate(total=Count('causa')).order_by('causa')

    sin_rechazo = base.filter(SIN_RECHAZO).count()
    informacion = base.filter(causa=INFORMACION).count()
    entrega = base.filter(causa=ENTREGA).count()
    otro = base.filter(causa=OTRO).count()

    con_rechazo = base.filter(CON_RECHAZO).count()
    acta = base.filter(causa=ACTA).count()
    id = base.filter(causa=IDENTIFICACION).count()
    dom = base.filter(causa=COMPROBANTE).count()
    ficha = base.filter(causa=FICHA).count()
    edad = base.filter(causa=EDAD).count()
    huella = base.filter(causa=HUELLA).count()

    data = {
        'total': base.count(),

        'sin_rechazo': sin_rechazo,
        'informacion': informacion,
        'entrega': entrega,
        'otro': otro,

        'con_rechazo': con_rechazo,
        'acta': acta,
        'id': id,
        'dom': dom,
        'ficha': ficha,
        'edad': edad,
        'huella': huella,

        'txt_causas': CAUSAS,
        'inicio': base.last(),
        'fin': base.first()
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'kpi_path': True})
        context.update(self.data)
        return context


class MesasAdd(CreateView):
    model = Registro
    form_class = MesaForm
    success_url = reverse_lazy('mesas:add')

    def get_initial(self):
        last = Registro.objects.last()
        initial = super(MesasAdd, self).get_initial()
        initial['modulo'] = last.modulo
        initial['fecha'] = last.fecha
        initial['lugar'] = last.lugar
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        messages.success(
            self.request,
            f'El registro ({self.object.fecha} - {self.object.get_sexo_display()} - {self.object.get_causa_display()}) \
             <strong>se guardó</strong> correctamente'
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'kpi_path': True})
        return context

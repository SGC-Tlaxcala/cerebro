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
from apps.mesas.models import Registro, CAUSAS, INFORMACION, ENTREGA, OTRO
from apps.mesas.forms import MesaForm

no_info = Q(causa=INFORMACION)
no_otro = Q(causa=OTRO)
no_entrega = Q(causa=ENTREGA)


class MesasIndex(TemplateView):
    template_name = 'mesas/index.html'

    base = Registro.objects.all().exclude(no_info).exclude(no_otro).exclude(no_entrega).order_by('fecha', 'id')
    sexo = base.values('sexo').annotate(total=Count('sexo'))
    causas = base.values('causa').annotate(total=Count('causa')).order_by('causa')

    data = {
        'sexo': sexo,
        'causas': causas,
        'txt_causas': CAUSAS,
        'inicio': base.first(),
        'fin': base.last()
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

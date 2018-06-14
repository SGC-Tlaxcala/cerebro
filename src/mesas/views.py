# coding: utf-8
#         app: mesa de atención
#      module: vistas
#        date: jueves, 14 de junio de 2018 - 09:06
# description: Vistas para la app de mesas de atención
# pylint: disable=W0613,R0201,R0903

from django.contrib import messages
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from mesas.models import Registro
from mesas.forms import MesaForm


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

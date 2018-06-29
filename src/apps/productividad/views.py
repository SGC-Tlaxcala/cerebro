# coding: utf-8
#         app: productividad
#      module: vistas
#        date: viernes, 29 de junio de 2018 - 12:44
# description:
# pylint: disable=W0613,R0201,R0903


from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, CreateView
from .forms import ReporteSemanalForm, CifrasForm, ReporteCifrasFormSet


class ProductividadIndex(CreateView):
    form_class = ReporteSemanalForm
    template_name = "productividad/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'formset': ReporteCifrasFormSet})
        return context

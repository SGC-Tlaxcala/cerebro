# coding: utf-8
#         app: docs
#      module: Vistas
#        date: miércoles, 06 de junio de 2018 - 10:49
# description: Vistas de la app de documentación
# pylint: disable=W0613,R0201,R0903

from watson import search as watson
from django.db.models import Q
from django.views.generic import (
    ListView,
    TemplateView,
    DetailView
)
from apps.docs.models import Documento, Proceso


class IndexList(ListView):
    model = Documento
    template_name = 'docs/portada2.html'
    context_object_name = 'docs'

    def get_queryset(self):
        return Documento.objects.filter(Q(activo=True)).order_by('proceso', 'nombre')


class DocDetail(DetailView):
    model = Documento
    context_object_name = 'doc'


class ProcesoList(DetailView):
    model = Proceso
    context_object_name = 'proceso'


class Buscador(TemplateView):
    template_name = 'docs/busqueda.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        resultados = {}
        if query:
            resultados = watson.search(query)
        context.update({
            'resultados': resultados,
            'query': query
        })
        return context

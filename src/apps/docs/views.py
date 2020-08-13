# coding: utf-8
#         app: docs
#      module: Vistas
#        date: miércoles, 06 de junio de 2018 - 10:49
# description: Vistas de la app de documentación
# pylint: disable=W0613,R0201,R0903

from watson import search as watson
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import (
    ListView,
    TemplateView,
    DetailView
)
from django.views.generic.edit import CreateView
from django.template.defaultfilters import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.docs.models import Documento, Proceso, Tipo, Revision
from apps.docs.forms import DocForm, ProcesoForm, TipoForm, VersionForm


class IndexList(ListView):
    model = Documento
    template_name = 'docs/portada2.html'
    context_object_name = 'docs'

    def get_queryset(self):
        return Documento.objects.filter(Q(activo=True)).\
            order_by('proceso', 'nombre')


class DocDetail(DetailView):
    model = Documento
    context_object_name = 'doc'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'version': VersionForm
        })
        return context


class SetupDoc(TemplateView):
    template_name = 'docs/setup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        process = Proceso.objects.all()
        types = Tipo.objects.all()
        context.update({
            'process_form': ProcesoForm,
            'process': process,
            'types_form': TipoForm,
            'types': types
        })
        return context


class DocAdd(CreateView):
    model = Documento
    form_class = DocForm

    def form_valid(self, form):
        self.document = form.save(commit=False)
        self.document.autor = self.request.user
        self.document.slug = slugify(self.document.nombre)
        self.document.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('docs:detalle', args=(self.object.id,))


class RevisionAdd(LoginRequiredMixin, CreateView):
    model = Revision
    form_class = VersionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doc = Documento.objects.get(pk=self.kwargs['pk'])
        context.update({
            'doc': doc
        })
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.autor = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('docs:detalle', args=(self.kwargs['pk'],))


class ProcesoList(DetailView):
    model = Proceso
    context_object_name = 'proceso'


class ProcessAdd(CreateView):
    model = Proceso
    fields = ['proceso', 'slug']
    success_url = reverse_lazy('docs:setup')


class TipoAdd(CreateView):
    model = Tipo
    fields = ['tipo', 'slug']
    success_url = reverse_lazy('docs:setup')


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

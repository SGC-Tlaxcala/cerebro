"""
Aquí se controlan las vistas de la aplicación docs.

Incluye las siguientes vistas:
- Reportes
- IndexLMD (Lista Maestra de Documentos)
- IndexList, la portada
- DocDetail, el detalle de un documento
- DocAdd, para agregar un documento
- RevisionAdd, para agregar una revisión de un documento
- ProcesoList, la lista de procesos
- ProcesoAdd, para agregar un proceso
- TipoAdd, para agregar un tipo de documento
- Buscador, el buscador de documentos
"""

from watson import search as watson
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import (ListView, TemplateView, DetailView)
from django.views.generic.edit import CreateView
from django.template.defaultfilters import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.docs.models import Documento, Proceso, Tipo, Revision
from apps.docs.forms import DocForm, ProcesoForm, TipoForm, VersionForm


class Reportes(ListView):
    """
    Clase Reportes.

    Crea una vista tipo ListView que muestra los documentos en el
    grupo 'reportes'.
    """

    model = Documento
    context_object_name = 'docs'

    def get_queryset(self):
        """La consulta que devuelve los documentos con slug 'RPT'."""
        return Documento.objects.filter(tipo__slug='RPT').order_by('id')


class IndexLMD(ListView):
    """
    Índice de la Lista Maestra de Documentos.

    Genera una ListView con los documentos en el proceso LMD.
    Cambiará en agosto de 2023 a una propiedad del documento.
    """

    model = Documento
    context_object_name = 'docs'

    def get_queryset(self):
        """Genera la consulta de la LMD."""
        return Documento.objects.filter(proceso__slug='lmd').order_by('id')


class IndexList(ListView):
    """
    Vista que genera la portada de la app docs.

    Se agrega al contexto el queryset `docs`.
    """

    model = Documento
    template_name = 'docs/portada2.html'
    context_object_name = 'docs'

    def get_queryset(self):
        """Consulta para la portada. Todos los documentos."""
        return Documento.objects.filter(Q(activo=True)).\
            order_by('proceso', 'nombre')


class DocDetail(DetailView):
    """
    Es la vista para el detalle de documentos.

    Agrega al contexto `version` para el completado de la
    nueva revisión.
    """

    model = Documento
    context_object_name = 'doc'

    def get_context_data(self, **kwargs):
        """Agrega la variable `version` al contexto de la vista."""
        context = super().get_context_data(**kwargs)
        context.update({'version': VersionForm})
        return context


class SetupDoc(TemplateView):
    """
    Crea un nuevo documento.

    Esta clase crea un nuevo documento, establece su tipo y el proceso al que
    pertenece y agrega la primera versión.
    """

    template_name = 'docs/setup.html'

    def get_context_data(self, **kwargs):
        """
        Agrega las siguientes variables al contexto.

        - `process_form`, es el formulario para crear un nuevo proceso.
        - `process`, el proceso al que pertenece el documento.
        - `types_form`: el formulario para agregar un nuevo tipo.
        - `type`: El tipo de documento.
        """
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
    """Formulario para agregar un documento."""

    model = Documento
    form_class = DocForm

    def form_valid(self, form):
        """Validación del formulario."""
        self.document = form.save(commit=False)
        self.document.autor = self.request.user
        self.document.slug = slugify(self.document.nombre)
        self.document.save()
        return super().form_valid(form)

    def get_success_url(self):
        """Redirección en caso de éxito."""
        return reverse_lazy('docs:detalle', args=(self.object.id, ))


class RevisionAdd(LoginRequiredMixin, CreateView):
    model = Revision
    form_class = VersionForm

    def dispatch(self, request, *args, **kwargs):
        self.doc = Documento.objects.get(pk=kwargs['pk'])
        return super(RevisionAdd, self).dispatch(request, *args, **kwargs)

    def get_inital(self):
        super(RevisionAdd, self).get_initial()
        revision = self.doc.revision_set.order_by('-revision')[0].revision + 1
        self.initial['revision'] = revision + 1
        return self.initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'doc': self.doc})
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.autor = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('docs:detalle', args=(self.kwargs['pk'], ))


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
        context.update({'resultados': resultados, 'query': query})
        return context

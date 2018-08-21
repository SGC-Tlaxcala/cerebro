# coding: utf-8
#         app: docs
#      module: Vistas
#        date: miércoles, 06 de junio de 2018 - 10:49
# description: Vistas de la app de documentación
# pylint: disable=W0613,R0201,R0903

from watson import search as watson
from django.http import Http404
from django.shortcuts import render
from django.db.models import Q
from django.views.generic import (
    TemplateView,
    DetailView
)
from apps.docs.models import Documento, Tipo, Proceso


def index(request):
    template_name = 'docs/portada2.html'
    try:
        docs = Documento.objects.filter(Q(activo=True)).order_by('proceso', 'nombre').prefetch_related()
    except Documento.DoesNotExist:
        raise Http404('No hay documentos')
    context = {
        'docs': docs
    }
    return render(request, template_name, context)


class DocIndex(TemplateView):
    template_name = 'docs/portada.html'
    # Consultas
    tipos = Tipo.objects.exclude(Q(slug='pro') | Q(slug='doc'))
    docs = (Q(tipo__slug='doc') | Q(tipo__slug='pro'))

    doc = Documento.objects.filter(Q(activo=True)).order_by('proceso', 'nombre').prefetch_related()
    los_docs = doc.filter(docs).prefetch_related()
    los_regs = doc.filter(tipo__slug='registros').prefetch_related()
    las_ints = doc.filter(tipo__slug='int').prefetch_related()
    los_fmts = doc.filter(tipo__slug='fmt').prefetch_related()
    los_exts = doc.filter(tipo__slug='externo').prefetch_related()
    las_stn = doc.filter(tipo__slug='stn').prefetch_related()
    los_coc = doc.filter(tipo__slug='coc').prefetch_related()

    docs = {
        'tipos': tipos,
        'los_docs': los_docs,
        'los_regs': los_regs,
        'las_ints': las_ints,
        'los_fmts': los_fmts,
        'los_exts': los_exts,
        'title': 'Control de Documentos',
        'las_stn': las_stn,
        'los_coc': los_coc
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.docs)
        return context


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


# @login_required
# def agregar_documento (request):
#     if request.method == 'POST':
#         autor = Documento(autor = request.user)
#         form = DocumentoForm (request.POST, instance=autor)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.save()
#             form.save_m2m()
#             doc = obj.pk
#             ruta = '/docs/%s/control' % doc
#             return HttpResponseRedirect(ruta)
#     else:
#         form = DocumentoForm()
#     return render_to_response ('2014/docs/agregar_documento.html', {
#         'form':form,
#         'title': 'Agregar un nuevo documento',},
#         context_instance=RequestContext(request)
#     )
#
# @login_required
# def agregar_control(request, doc):
#     if request.method == 'POST':
#         form = RevisionForm(request.POST, request.FILES)
#         if form.is_valid():
#             instancia = form.save(commit=False)
#             instancia.autor = request.user
#             instancia.save()
#             handle_uploaded_file(request.FILES['archivo'], instancia)
#             ruta = '/docs/%s/detalles' % doc
#             return HttpResponseRedirect(ruta)
#     else:
#         form = RevisionForm()
#         form.initial['documento'] = doc
#     return render_to_response ('2014/docs/agregar_control.html', {
#         'form':form, 'doc':doc,
#         'title': 'Agregar un nuevo documento',
#         },
#         context_instance=RequestContext(request)
#     )
#
#
# @render_to('2014/docs/editar_control.html')
# @login_required
# def editar_control(request, rev):
#     edicion = get_object_or_404 (Revision, pk=rev)
#     form = RevisionForm(request.POST or None, instance=edicion)
#     if form.is_valid():
#         edicion = form.save()
#         edicion.save()
#         if request.FILES.has_key('archivo'):
#             archivo = request.FILES['archivo']
#             handle_uploaded_file(archivo, edicion)
#         else:
#             archivo = edicion.archivo
#             editar_revision(archivo, edicion)
#         ruta = '/docs/%s/detalles' % edicion.documento.id
#         return redirect (ruta)
#     return { 'form': form, 'title':'Editando revisión' }

#

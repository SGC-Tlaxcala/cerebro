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

from datetime import datetime
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from watson import search as watson
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import (ListView, TemplateView, DetailView, FormView)
from django.views.generic.edit import CreateView, UpdateView
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.contrib import messages
from apps.docs.models import Documento, Proceso, Tipo, Revision, Reporte, Notificacion
from apps.profiles.models import Profile
from apps.docs.forms import (
    DocForm,
    ProcesoForm,
    ReporteForm,
    TipoForm,
    VersionForm,
    PanicResolveForm
)


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

    def __str__(self):
        return self.__class__.__name__


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
        return Documento.objects.filter(lmd=True, activo=True).order_by('id')

    def __str__(self):
        return self.__class__.__name__

    def get_context_data(self, **kwargs):
        """Agrega la variable `active` al contexto de la vista."""
        context = super().get_context_data(**kwargs)
        # Buscamos los reportes que existan en el documento actual
        # y los agregamos al contexto
        context['activeLMD'] = True
        context['panicButton'] = True
        return context


class IndexLDP(ListView):
    """Lista de documentos por proceso."""

    model = Documento
    template_name = 'docs/ldp.html'
    context_object_name = 'docs'

    def get_queryset(self):
        """Genera la consulta de la LMD."""
        return Documento.objects\
            .filter(lmd=False, activo=True)\
            .order_by('proceso', 'tipo')

    def get_context_data(self, **kwargs):
        """Agrega la variable `active` al contexto de la vista."""
        context = super().get_context_data(**kwargs)
        # Buscamos los reportes que existan en el documento actual
        # y los agregamos al contexto
        context['activeLDP'] = True
        context['panicButton'] = True
        return context


class IndexLDT(ListView):
    """Lista de documentos por tipo."""

    model = Documento
    template_name = 'docs/ldt.html'
    context_object_name = 'docs'

    def get_context_data(self, **kwargs):
        """Agregamos la variable panicButton al contexto de la vista."""
        context = super().get_context_data(**kwargs)
        context['panicButton'] = True
        return context

    def get_queryset(self):
        """Genera la consulta de la LMD."""
        return Documento.objects\
            .filter(lmd=False, activo=True).order_by('tipo', 'proceso', 'id')


class IndexList(ListView):
    """
    Vista que genera la portada de la app docs.

    Se agrega al contexto el queryset `docs`.
    """

    model = Documento
    template_name = 'docs/portada.html'
    context_object_name = 'docs'

    def get_context_data(self, **kwargs):
        """Agregamos la variable panicButton al contexto de la vista."""
        context = super().get_context_data(**kwargs)
        context['panicButton'] = True
        return context

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
        # Buscamos los reportes que existan en el documento actual
        # y los agregamos al contexto
        context['reportes'] = Reporte.objects.filter(documento=self.kwargs['pk'])
        context['panicButton'] = True
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
    """Formulario para crear una nueva revisión de un documento."""

    model = Revision
    form_class = VersionForm

    def dispatch(self, request, *args, **kwargs):
        """Crea un nuevo documento en el formulario."""
        self.doc = Documento.objects.get(pk=kwargs['pk'])
        return super(RevisionAdd, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        super(RevisionAdd, self).get_initial()
        try:
            revision = self.doc.revision_set.order_by('-revision')[0].revision + 1
        except IndexError:
            revision = 0
        fecha = datetime.today()
        self.initial['revision'] = revision
        self.initial['f_actualizacion'] = fecha
        return self.initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'doc': self.doc})
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.documento = self.doc
        self.object.autor = self.request.user
        self.object.save()

        if form.cleaned_data['notificacion_urgente']:
            # Obtener los perfiles de los usuarios que desean recibir notificaciones
            perfiles = Profile.objects.filter(
                recibe_notificaciones=True, 
                user__email__isnull=False
            ).select_related('user')

            if perfiles:
                asunto = f"Notificación Urgente: Actualización del documento {self.doc.clave()}"
                correos_enviados = []
                
                for perfil in perfiles:
                    nombre_usuario = perfil.user.get_full_name() or perfil.user.username
                    
                    # Renderizar la plantilla de correo para cada usuario
                    cuerpo_html = render_to_string('docs/notificacion_urgente.html', {
                        'documento': self.doc,
                        'revision': self.object,
                        'nombre_usuario': nombre_usuario,
                    })

                    try:
                        send_mail(
                            subject=asunto,
                            message='',  # El mensaje de texto plano no es necesario si se envía HTML
                            from_email=None,  # Usará DEFAULT_FROM_EMAIL de settings.py
                            recipient_list=[perfil.user.email],
                            html_message=cuerpo_html,
                            fail_silently=False,
                        )
                        correos_enviados.append(perfil.user.email)

                    except Exception as e:
                        messages.error(self.request, f"Error al enviar la notificación a {perfil.user.email}: {e}")
                
                if correos_enviados:
                    # Marcar la notificación como enviada
                    self.object.notificacion_enviada = True
                    self.object.fecha_notificacion = datetime.now()
                    self.object.save()

                    # Crear un registro de la notificación
                    notif = Notificacion.objects.create(
                        tipo='U',
                        asunto=asunto,
                        cuerpo_html="Correo personalizado enviado a cada destinatario.", # El cuerpo es genérico aquí
                        destinatarios=", ".join(correos_enviados),
                    )
                    notif.revisiones.add(self.object)

                    messages.success(self.request, f"Se enviaron {len(correos_enviados)} notificaciones urgentes correctamente.")
                else:
                    messages.error(self.request, "No se pudo enviar ninguna notificación urgente.")

            else:
                messages.warning(self.request, "No hay usuarios configurados para recibir notificaciones urgentes.")

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('docs:detalle', args=(self.kwargs['pk'], ))


class ProcesoList(DetailView):
    """Lista de documentos por proceso."""
    model = Proceso
    context_object_name = 'proceso'


class ProcessAdd(CreateView):
    """Formulario para agregar un nuevo proceso."""
    model = Proceso
    fields = ['proceso', 'slug']
    success_url = reverse_lazy('docs:setup')


class TipoAdd(CreateView):
    """Formulario para agregar un nuevo tipo de documento."""
    model = Tipo
    fields = ['tipo', 'slug']
    success_url = reverse_lazy('docs:setup')


class Buscador(TemplateView):
    """Vista para el buscador de documentos."""
    template_name = 'docs/busqueda.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        resultados = {}
        if query:
            resultados = watson.search(query)
        context.update({'resultados': resultados, 'query': query})
        return context


class PanicButtonView(FormView):
    """Vista para el botón de pánico."""
    template_name = 'docs/panic.html'
    form_class = ReporteForm

    def get_context_data(self, **kwargs):
        """Agregamos el documento_id obtenido mediante el parámetro
        pk de la URL al contexto de la vista."""
        context = super(PanicButtonView, self).get_context_data(**kwargs)
        context['documento'] = Documento.objects.get(pk=self.kwargs['pk'])
        return context

    def get_initial(self):
        """Inicializamos el formulario con el documento actual
            para usarlo en el templates y el registro que se guarda
            en la base de datos."""
        initial = super(PanicButtonView, self).get_initial()
        initial['documento'] = self.kwargs['pk']
        return initial

    # Guardamos el reporte en la base de datos
    def form_valid(self, form):
        """El Documento en el contexto se agrega al campo documento
        del formulario."""
        form.instance.documento = Documento.objects.get(pk=self.kwargs['pk'])
        # Si el correo no termina en '@ine.mx' se rechaza el formulario
        if not form.instance.correo.endswith('@ine.mx'):
            return self.form_invalid(form)
        # Si el formulario es válido, se guarda en la base de datos
        else:
            form.save()
        return super(PanicButtonView, self).form_valid(form)

    # Redirigimos a la página de éxito
    def get_success_url(self):
        return reverse_lazy('docs:panic_success')


class ReportesList(ListView):
    """Lista de reportes."""
    model = Reporte
    template_name = 'docs/panic_reportes.html'

    # Agregamos los reportes al contexto de la vista
    def get_context_data(self, **kwargs):
        context = super(ReportesList, self).get_context_data(**kwargs)
        context['pendientes'] = Reporte.objects.filter(resuelto=False).order_by('-created')
        context['resueltos'] = Reporte.objects.filter(resuelto=True).order_by('-resuelto_en')
        return context


class PanicResolve(LoginRequiredMixin, UpdateView):
    model = Reporte
    template_name = 'docs/panic_resolve.html'
    success_url = reverse_lazy('docs:panic_reportes')
    form_class = PanicResolveForm

    # Agregamos el reporte al contexto de la vista
    def get_context_data(self, **kwargs):
        context = super(PanicResolve, self).get_context_data(**kwargs)
        context['reporte'] = Reporte.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save(commit=False)
        self.object.documento = Reporte.objects.get(pk=self.kwargs['pk']).documento
        self.object.resuelto_por = self.request.user
        self.object.resuelto_en = datetime.now()
        self.object.resolucion = form.cleaned_data['resolucion']
        self.object.resuelto = form.cleaned_data['resuelto']
        self.object.save()
        return super().form_valid(form)


# reportes_context - un custom context processor para agregar el conteo de reportes
# a todas las vistas
def reportes_context(request):
    if request.user.is_authenticated:
        reportes = Reporte.objects.filter(resuelto=False).count()
        return {'panic_reports': reportes}
    else:
        return {}

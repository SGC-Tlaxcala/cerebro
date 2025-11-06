from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.db.models import OuterRef, Subquery
from .models import Plan, Accion, Seguimiento
from .forms import PlanForm


class PASIndex(ListView):
    model = Plan
    template_name = 'pas/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plan_list = Plan.objects.all()
        # Subquery to get the latest estado for each Accion
        latest_estado = Seguimiento.objects.filter(
            accion=OuterRef('pk')
        ).order_by('-fecha').values('estado')[:1]
        # Annotate each Accion with the latest estado
        action_list = Accion.objects.annotate(
            latest_estado=Subquery(latest_estado)
        ).order_by('latest_estado', 'fecha_fin')

        for plan in plan_list:
            cerradas = 0
            abiertas_en_tiempo = 0
            abiertas_fuera_de_tiempo = 0

            for accion in plan.accion_set.all():
                estado = accion.get_estado
                if estado == 'Cerrada':
                    cerradas += 1
                elif estado == 'Abierta en Tiempo':
                    abiertas_en_tiempo += 1
                elif estado == 'Abierta Fuera de Tiempo':
                    abiertas_fuera_de_tiempo += 1

            plan.cerradas = cerradas
            plan.abiertas_en_tiempo = abiertas_en_tiempo
            plan.abiertas_fuera_de_tiempo = abiertas_fuera_de_tiempo

        context['plan_list'] = plan_list
        context['action_list'] = action_list
        return context

class PASAdd(CreateView):
    model = Plan
    form_class = PlanForm
    template_name = 'pas/add.html'
    success_url = reverse_lazy('pas:index')

    def dispatch(self, request, *args, **kwargs):
        if request.headers.get('HX-Request') and request.GET.get('close'):
            return HttpResponse('')
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['pas/partials/_plan_form.html']
        return super().get_template_names()

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        if self.request.headers.get('HX-Request'):
            redirect_url = str(self.get_success_url())
            return HttpResponse('', status=204, headers={'HX-Redirect': redirect_url})
        return response

    def form_invalid(self, form):
        if self.request.headers.get('HX-Request'):
            return self.render_to_response(self.get_context_data(form=form), status=422)
        return super().form_invalid(form)


class PASDetail(DetailView):
    model = Plan


class PASAction(DetailView):
    model = Accion

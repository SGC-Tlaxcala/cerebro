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

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user  # Asignar el usuario actual
        print(f'-- Este es el usuario: {obj.user}')
        obj.save()
        return super().form_valid(form)


class PASDetail(DetailView):
    model = Plan


class PASAction(DetailView):
    model = Accion

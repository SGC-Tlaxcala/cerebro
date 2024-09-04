from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Plan, Accion
from .forms import PlanForm


class PASIndex(ListView):
    model = Plan
    template_name = 'pas/index.html'


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


# @render_to('seguimiento.html')
# def seguimiento(request, id):
#     accion = Accion.objects.get(pk=id)
#     return {
#         'title': 'Lista de actividades de seguimiento',
#         'accion': accion
#     }

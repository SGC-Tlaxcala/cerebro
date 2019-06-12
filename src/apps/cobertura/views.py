from django.views.generic.list import ListView
from apps.cobertura.models import Cobertura


class Portada(ListView):
    template_name = 'cobertura/index.html'
    model = Cobertura
    ordering = ['fecha', ]

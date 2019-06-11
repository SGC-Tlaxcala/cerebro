from django.views.generic.list import ListView
from apps.aprobacion.models import Aprobacion


class Portada(ListView):
    model = Aprobacion
    ordering = ['fecha', 'mac']

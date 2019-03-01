from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from apps.incidencias.models import Incidencia


class Portada(ListView):
    model = Incidencia


class EventoDetail(DetailView):
    model = Incidencia

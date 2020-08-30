from django.views.generic.list import ListView
from apps.cobertura.models import Cobertura
import datetime


class Portada(ListView):
    template_name = 'cobertura/index.html'
    model = Cobertura
    ordering = ['fecha', ]

    def get_queryset(self):
        query = Cobertura.objects.filter(fecha__gte=datetime.date(2019,10,1))
        return query

from datetime import datetime

from django.views import View
from django.shortcuts import render
from django.db.models import Sum

from apps.productividad.models import PronosticoTramites, Cifras


YEAR = 2019
YEARS = (2018, 2019)

pronostico = PronosticoTramites.objects.all().filter().filter(year=2019)


class Index(View):
    template_name = 'mc/index.html'

    def __init__(self):
        super(View, self).__init__()
        self.year = YEAR
        self.years = YEARS
        self.pronostico_estatal = 0
        self.pronostico = None
        self.cifras_estatal = None
        self.cifras = None
        self.entregas = None
        self.periodo = {}
        self.current_year = int(datetime.now().year)

    def dispatch(self, request, *args, **kwargs):
        self.year = self.request.GET.get("year", YEAR)
        self.pronostico = PronosticoTramites.objects.all().filter().filter(year=2019)
        for d in self.pronostico:
            print(d)
            self.pronostico_estatal += d.tramites
        self.cifras_estatal = Cifras.objects\
            .filter(reporte_semanal__fecha_corte__year=2019)\
            .aggregate(suma_modulo=Sum('tramites'))
        self.cifras = Cifras.objects \
            .filter(reporte_semanal__fecha_corte__year=2019) \
            .values('distrito') \
            .order_by('distrito') \
            .annotate(suma_modulo=Sum('tramites'))
        self.entregas = Cifras.objects.values('distrito')\
            .filter(reporte_semanal__fecha_corte__year=self.year)\
            .order_by('distrito')\
            .annotate(entregas_distrito=Sum('credenciales_entregadas_actualizacion'))
        return super(Index, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        data = {
            'pronostico': self.pronostico,
            'pronostico_estatal': self.pronostico_estatal,
            'cifras': self.cifras,
            'cifras_estatal': self.cifras_estatal['suma_modulo'],
            'faltantes': self.pronostico_estatal - self.cifras_estatal['suma_modulo']
        }
        return render(request, self.template_name, data)

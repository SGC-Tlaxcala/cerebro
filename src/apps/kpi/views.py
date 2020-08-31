from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = "kpi/index.html"


class Capacitacion(TemplateView):
    template_name = "kpi/capacitacion.html"


class Concilia(TemplateView):
    template_name = 'kpi/concilia.html'


class Supervisiones(TemplateView):
    template_name = 'kpi/supervisiones.html'


class Mantenimiento(TemplateView):
    template_name = 'kpi/mantenimiento.html'


class Contratacion(TemplateView):
    template_name = 'kpi/contratacion.html'


class Gasto(TemplateView):
    template_name = 'kpi/gasto.html'


class Encuestas(TemplateView):
    template_name = 'kpi/encuestas.html'

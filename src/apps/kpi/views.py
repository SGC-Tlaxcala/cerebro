from django.views.generic import TemplateView

# Create your views here.
class Index(TemplateView):
    template_name = "kpi/index.html"


class Capacitacion(TemplateView):
    template_name = "kpi/capacitacion.html"


class Concilia(TemplateView):
    template_name = 'kpi/concilia.html'

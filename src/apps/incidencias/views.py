from django.views.generic import TemplateView


class Portada(TemplateView):
    template_name = 'incidencias/index.html'

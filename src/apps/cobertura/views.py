from django.views.generic import TemplateView


class Portada(TemplateView):
    template_name = 'cobertura/index.html'

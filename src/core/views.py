"""Vistas iniciales para el SGC."""

from django.views.generic import TemplateView


class Index(TemplateView):
    """Vista del índice del SGC."""
    template_name = 'index.html'

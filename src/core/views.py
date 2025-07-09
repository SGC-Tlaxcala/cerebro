"""Vistas iniciales para el SGC."""

from django.views.generic import TemplateView
from apps.kpi.models import Campaign


class Index(TemplateView):
    """Vista del índice del SGC."""
    template_name = 'index.html'

    # Se agrega al contexto Campaigns.actual(2025, 'CAP')
    def get_context_data(self, **kwargs):
        """Agrega el contexto necesario para la vista."""
        context = super().get_context_data(**kwargs)
        context['cap'] = Campaign.actual(2025, 'CAP')
        return context

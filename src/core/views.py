"""Vistas iniciales para el SGC."""

from django.views.generic import TemplateView
from apps.kpi.models import Campaign


class Index(TemplateView):
    """Vista del índice del SGC."""
    template_name = 'cerebro/index.html'

    # Se agrega al contexto Campaigns.actual(2025, 'CAP')
    def get_context_data(self, **kwargs):
        """Agrega el contexto necesario para la vista."""
        imagen = {
            'title': 'Imagen Institucional',
            'year': 2025,
            'semestre': '01',
            'mac_imagen': 2,
            'mac_totales': 6,
            'meta': 30,
            'avance': 30,
        }
        context = super().get_context_data(**kwargs)
        context['cap'] = Campaign.actual(2025, 'CAP')
        context['imagen'] = imagen
        return context

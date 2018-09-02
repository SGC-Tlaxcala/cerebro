# cofing: utf-8
"""Vistas para evaluar al proveedor."""


from django.db.models import Avg
from django.views import View
from django.shortcuts import render
from apps.cecyrd.models import Tramites


class CecyrdIndex(View):
    """Vista para la portada de control de proveedor."""
    template_name = 'cecyrd/index.html'

    def get(self, request, *args, **kwargs):
        """Función del verbo GET."""
        tramites = Tramites.objects\
            .exclude(tramo_entrega__isnull=True)\
            .values('fecha_tramite__date')\
            .annotate(disponible=Avg('tramo_disponible'))
        data = {
            'tramites': tramites,
            'kpi_path': True,
            'title': 'Control de tiempo de entrega'
        }
        return render(request, self.template_name, data)

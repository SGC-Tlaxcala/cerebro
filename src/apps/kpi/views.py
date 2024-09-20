from django.views.generic import TemplateView
from .models import KPI


class KpiIndex(TemplateView):
    template_name = 'kpi/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'KPI'
        context['kpis'] = KPI.objects.filter(active=True)
        context['is_htmx'] = self.request.headers.get('HX-Request') is not None
        return context

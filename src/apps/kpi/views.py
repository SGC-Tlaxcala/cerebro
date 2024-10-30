from django.views.generic import TemplateView, DetailView
from .models import KPI, Period


class KpiIndex(TemplateView):
    template_name = 'kpi/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'KPI'
        context['kpis'] = KPI.objects.filter(active=True)
        context['is_htmx'] = self.request.headers.get('HX-Request') is not None
        return context


class KPIDetail(DetailView):
    model = KPI
    template_name = 'kpi/kpi_detail.html'
    context_object_name = 'kpi'

    def get_queryset(self):
        return self.model.objects.filter(active=True, pk=self.kwargs['pk'])


class PeriodDetail(DetailView):
    model = Period
    template_name = 'kpi/period_detail.html'
    context_object_name = 'period'

    def get_queryset(self):
        return self.model.objects.filter(active=True, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chart'] = self.kwargs['chart']
        return context

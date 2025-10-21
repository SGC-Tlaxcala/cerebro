from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
    VozMACAdd,
    VozMACIndex,
    sales_metrics,
    likert_by_mac,
)

app_name = 'vozmac'
urlpatterns = [
    path('', VozMACIndex.as_view(), name='index'),
    path('add/', login_required(VozMACAdd.as_view()), name='add'),
    path('api/metrics/sales/', sales_metrics, name='api_metrics_sales'),
    path('api/metrics/likert-by-mac/', likert_by_mac, name='api_metrics_likert_by_mac'),
]

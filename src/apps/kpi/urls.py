from django.urls import path
from .views import KpiIndex, KPIDetail, PeriodDetail

app_name = 'kpi'

urlpatterns = [
    path('kpi/period/<int:pk>/<str:chart>/', PeriodDetail.as_view(), name='period'),
    path('kpi/<int:pk>/', KPIDetail.as_view(), name='detail'),
    path('', KpiIndex.as_view(), name='index'),
]

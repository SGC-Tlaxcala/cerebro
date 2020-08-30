from django.urls import path
from apps.kpi.views import Index, Capacitacion, Concilia


app_name = 'kpi'
urlpatterns = [
    path('capacitacion', Capacitacion.as_view(), name='capacitacion'),
    path('concilia', Concilia.as_view(), name='concilia'),
    path('', Index.as_view(), name='index')
]


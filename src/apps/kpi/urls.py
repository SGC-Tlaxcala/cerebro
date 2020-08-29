from django.urls import path
from apps.kpi.views import Index, Capacitacion


app_name = 'kpi'
urlpatterns = [
    path('capacitacion', Capacitacion.as_view(), name='capacitacion'),
    path('', Index.as_view(), name='index')
]


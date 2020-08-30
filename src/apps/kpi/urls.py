from django.urls import path
from apps.kpi.views import (Index,
                            Capacitacion, Concilia, Supervisiones,
                            Mantenimiento)


app_name = 'kpi'
urlpatterns = [
    path('capacitacion', Capacitacion.as_view(), name='capacitacion'),
    path('concilia', Concilia.as_view(), name='concilia'),
    path('supervisiones', Supervisiones.as_view(), name='supervisiones'),
    path('manteniento', Mantenimiento.as_view(), name='mantenimiento'),
    path('', Index.as_view(), name='index')
]


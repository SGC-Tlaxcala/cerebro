from django.urls import path
from apps.kpi.views import (Index,
                            Capacitacion, Concilia, Supervisiones,
                            Mantenimiento, Contratacion, Gasto,
                            Encuestas, Checklist, Cartografia,
                            Incidencias)


app_name = 'kpi'
urlpatterns = [
    path('capacitacion', Capacitacion.as_view(), name='capacitacion'),
    path('concilia', Concilia.as_view(), name='concilia'),
    path('supervisiones', Supervisiones.as_view(), name='supervisiones'),
    path('manteniento', Mantenimiento.as_view(), name='mantenimiento'),
    path('contratacion', Contratacion.as_view(), name='contratacion'),
    path('gasto', Gasto.as_view(), name='gasto'),
    path('encuestas', Encuestas.as_view(), name='encuestas'),
    path('checklist', Checklist.as_view(), name='checklist'),
    path('cartografia', Cartografia.as_view(), name='cartografia'),
    path('incidencias', Incidencias.as_view(), name='incidencias'),
    path('', Index.as_view(), name='index')
]

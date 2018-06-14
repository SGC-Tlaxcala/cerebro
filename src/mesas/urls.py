# coding: utf-8
#         app: mesas de atención
#      module: patrones de rutas
#        date: jueves, 14 de junio de 2018 - 09:11
# description: Patrones para rutas de la Mesa de Atención
# pylint: disable=W0613,R0201,R0903

from django.urls import path
from mesas.views import MesasAdd

app_name = 'mesas'
urlpatterns = [
    path('', MesasAdd.as_view(), name='add')
]

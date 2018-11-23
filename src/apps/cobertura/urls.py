# coding: utf-8
#         app: cobertura
#      module: urls.py
#        date: miércoles, 06 de junio de 2018 - 11:30
# description: Patrones de ruta de cobertura.
# pylint: disable=W0613,R0201,R0903


from django.urls import path
from apps.cobertura.views import Portada

app_name = 'cobertura'
urlpatterns = [
    path('', Portada.as_view(), name='index')
]

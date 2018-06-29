# coding: utf-8
#         app: productividad
#      module: urls.py
#        date: viernes, 29 de junio de 2018 - 12:47
# description: Patrones de búsqueda
# pylint: disable=W0613,R0201,R0903


from django.urls import path
from .views import ProductividadIndex

app_name = 'productividad'
urlpatterns = [
    path('', ProductividadIndex.as_view(), name='index')
]

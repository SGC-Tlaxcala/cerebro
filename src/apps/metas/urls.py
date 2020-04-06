# coding: utf-8
#         app: metas
#      module: urls
#        date: miércoles, 23 de mayo de 2018 - 11:11
# description: rutas
# pylint: disable=W0613,R0201,R0903


from django.urls import path
from apps.metas.views import MetasIndex, MetasAddRol

app_name = 'metas'
urlpatterns = [
    path('', MetasIndex.as_view(), name='index'),
    path('add_rol/', MetasAddRol.as_view(), name='add_rol')
]

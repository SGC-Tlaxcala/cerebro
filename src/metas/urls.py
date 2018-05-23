# coding: utf-8
#         app: metas
#      module: urls
#        date: miércoles, 23 de mayo de 2018 - 11:11
# description: rutas
# pylint: disable=W0613,R0201,R0903


from django.urls import path
from metas.views import index

app_name = 'metas'
urlpatterns = [
    path('', index, name='index_metas')
]
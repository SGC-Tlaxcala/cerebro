# coding: utf-8
#         app: metas
#      module: urls
#        date: miércoles, 23 de mayo de 2018 - 11:11
# description: rutas
# pylint: disable=W0613,R0201,R0903


from django.urls import path
from apps.metas.views import MetasIndex, MetasAddRole, MetasAddSite, MetasAddMember

app_name = 'metas'
urlpatterns = [
    path('', MetasIndex.as_view(), name='index'),
    path('add_rol/', MetasAddRole.as_view(), name='add_rol'),
    path('add_site/', MetasAddSite.as_view(), name='add_site'),
    path('add_member/', MetasAddMember.as_view(), name='add_member')
]

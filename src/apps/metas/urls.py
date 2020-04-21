# coding: utf-8
#         app: metas
#      module: urls
#        date: miércoles, 23 de mayo de 2018 - 11:11
# description: rutas
# pylint: disable=W0613,R0201,R0903


from django.urls import path
from apps.metas.views import MetasIndex, MetasAddRole, MetasAddSite, MetasAddMember, MetasAddGoal, CreateProof

app_name = 'metas'
urlpatterns = [
    path('', MetasIndex.as_view(), name='index'),
    path('add_role/', MetasAddRole.as_view(), name='add_role'),
    path('add_site/', MetasAddSite.as_view(), name='add_site'),
    path('add_member/', MetasAddMember.as_view(), name='add_member'),
    path('add_goal/', MetasAddGoal.as_view(), name='add_goal'),
    path('add_proof/', CreateProof.as_view(), name='add_proof')
]

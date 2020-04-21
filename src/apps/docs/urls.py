# coding: utf-8
#         app: docs
#      module: urls.py
#        date: miércoles, 06 de junio de 2018 - 11:30
# description: Patrones de ruta de documentos.
# pylint: disable=W0613,R0201,R0903


from django.urls import path
from apps.docs.views import IndexList, DocDetail, ProcesoList, ProcesoDetail, Buscador

app_name = 'docs'
urlpatterns = [
    path('', IndexList.as_view(), name='index'),
    path('<int:pk>/detalle', DocDetail.as_view(), name='detalle'),
    path('proceso/', ProcesoList.as_view(), name='proceso_list'),
    path('proceso/<slug:slug>', ProcesoDetail.as_view(), name='proceso_detail'),
    path('buscador/', Buscador.as_view(), name='buscador')
]

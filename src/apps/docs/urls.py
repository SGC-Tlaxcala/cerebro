# coding: utf-8
#         app: docs
#      module: urls.py
#        date: miércoles, 06 de junio de 2018 - 11:30
# description: Patrones de ruta de documentos.
# pylint: disable=W0613,R0201,R0903


from django.urls import path
from django.contrib.auth.decorators import login_required
from apps.docs.views import (
    IndexList, DocDetail, ProcesoList, Buscador, SetupDoc,
    ProcessAdd, TipoAdd, DocAdd, RevisionAdd
)

app_name = 'docs'
urlpatterns = [
    path('', IndexList.as_view(), name='index'),
    path('<int:pk>/detalle', DocDetail.as_view(), name='detalle'),
    path('proceso/<slug:slug>', ProcesoList.as_view(), name='proceso'),
    path('buscador/', Buscador.as_view(), name='buscador'),
    path('add/', login_required(DocAdd.as_view()), name='add'),
    path('setup/', login_required(SetupDoc.as_view()), name='setup'),
    path('process_add/', login_required(ProcessAdd.as_view()), name='process_add'),
    path('tipo_add/', login_required(TipoAdd.as_view()), name='tipo_add'),
    path('<int:pk>/add', RevisionAdd.as_view(), name='rev_add')
]

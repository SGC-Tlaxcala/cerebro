# coding: utf-8
#         app: docs
#      module: urls.py
#        date: miércoles, 06 de junio de 2018 - 11:30
# description: Patrones de ruta de documentos.
# pylint: disable=W0613,R0201,R0903


from django.urls import path
from docs.views import DocsIndex

app_name = 'docs'
urlpatterns = [
    path('', DocsIndex.as_view(), name='index')
]

# from django.conf.urls import patterns, url
#
# urlpatterns = patterns('docs.views'
#     , url (r'^$', 'index')                                     # muestra los documentos disponibles
#     , url (r'^(?P<doc>\d+)/detalles$', 'detalles')
#     , url (r'^add/$', 'agregar_documento')
#     , url (r'^(?P<doc>\d+)/control$', 'agregar_control')
#     , url (r'^revision/(?P<rev>\d+)', 'editar_control', name='editar_control')
#     , url (r'^buscador/$', 'docs_buscador', name='docs_buscador')
#     , url(r'^tag/(?P<tag>[-\w]+)$', 'docs_tags', name='tag')
#
#     , url (r'^proceso/(?P<proceso>[-\w]+)/$', 'docs_proceso', name='docs_proceso')
# )

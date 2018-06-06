# -*- encoding: utf-8 -*-
# nombre: cmi.docs.urls
#   desc: Patrones URL para la app docs

from django.conf.urls import patterns, url

urlpatterns = patterns('docs.views'
    , url (r'^$', 'index')                                     # muestra los documentos disponibles
    , url (r'^(?P<doc>\d+)/detalles$', 'detalles')
    , url (r'^add/$', 'agregar_documento')
    , url (r'^(?P<doc>\d+)/control$', 'agregar_control')
    , url (r'^revision/(?P<rev>\d+)', 'editar_control', name='editar_control')
    , url (r'^buscador/$', 'docs_buscador', name='docs_buscador')
    , url(r'^tag/(?P<tag>[-\w]+)$', 'docs_tags', name='tag')

    , url (r'^proceso/(?P<proceso>[-\w]+)/$', 'docs_proceso', name='docs_proceso')
)

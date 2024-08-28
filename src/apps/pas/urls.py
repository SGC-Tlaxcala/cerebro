# -*- coding: UTF-8 -*-

#         app: Control de planes de acción y seguimiento
#      modulo: pas.urls
# descripcion: Redirecciones para sgc-pas
#       autor: Javier Sanchez Toledano
#       fecha: miércoles, 1 de octubre de 2014

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'pas.views',
    url(r'^$', 'pas_home', name='pas'),
    url(r'^plan/(?P<id>\d+)$', 'plan', name='pas_plan'),
    url(r'^add/$', 'add', name='pas_add'),
    url(r'^seguimiento/(?P<id>\d+)$', 'seguimiento', name='seguimiento')
)

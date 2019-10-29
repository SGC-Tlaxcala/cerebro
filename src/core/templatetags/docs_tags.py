# -*- coding: UTF-8 -*-

#         app: org.toledano.yo
#      módulo: blog.templatetags.extra
# descripción: Funciones auxiliares para la plantilla
#       autor: Javier Sanchez Toledano
#       fecha: lunes, 21 de marzo de 2016

import re
from django import template

try:
    from apps.mesas.models import CAUSAS
except RuntimeError:
    pass

register = template.Library()

try:
    dict_causas = {key: value for key, value in CAUSAS}
except NameError:
    pass

@register.filter
def causas(causa):
    return dict_causas[causa]


@register.simple_tag
def current(request, pattern):
    try:
        if re.search(pattern, request.path):
            return 'active'
    except:
        return ''


@register.filter
def disqus_hash(value):
    return value.replace("/", "_")

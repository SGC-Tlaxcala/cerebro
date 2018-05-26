# coding: utf-8
#         app: metas
#      module: views
#        date: miércoles, 23 de mayo de 2018 - 11:05
# description: Vistas para las metas
# pylint: disable=W0613,R0201,R0903

from django.shortcuts import render
from metas.forms import MetasSPEForm


def index(request):
    form = MetasSPEForm()
    return render(request, 'metas/index.html', {'form': form})

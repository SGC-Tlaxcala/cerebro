# coding: utf-8
#         app: metas
#      module: views
#        date: miércoles, 23 de mayo de 2018 - 11:05
# description: Vistas para las metas
# pylint: disable=W0613,R0201,R0903

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Rol
from .forms import AddRolForm


class MetasIndex(TemplateView):
    template_name = 'metas/index.html'


class MetasAddRol(CreateView):
    model = Rol
    form_class = AddRolForm
    success_url = reverse_lazy('metas:add_rol')

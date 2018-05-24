# coding: utf-8
#         app: metas
#      module: forms
#       fecha: miércoles, 23 de mayo de 2018 - 10:22
# description: Formularios de las Metas SPEN
# pylint: disable=W0613,R0201,R0903

from crispy_forms.helper import FormHelper
from django import forms
from metas.models import Evidencia


class EvidenciaForm(forms.ModelForm):

    class Meta:
        model = Evidencia
        exclude = ['campos', ]

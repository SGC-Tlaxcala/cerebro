# coding: utf-8
#         app: metas
#      module: forms
#       fecha: miércoles, 23 de mayo de 2018 - 10:22
# description: Formularios de las Metas SPEN
# pylint: disable=W0613,R0201,R0903

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from metas.models import Evidencia, MetasSPE


class EvidenciaForm(forms.ModelForm):

    class Meta:
        model = Evidencia
        exclude = ['campos', ]


class MetasSPEForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MetasSPEForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Enviar'))

    class Meta:
        model = MetasSPE
        fields = '__all__'

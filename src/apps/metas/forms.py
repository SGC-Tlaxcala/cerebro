# coding: utf-8
#         app: metas
#      module: forms
#       fecha: miércoles, 23 de mayo de 2018 - 10:22
# description: Formularios de las Metas SPEN
# pylint: disable=W0613,R0201,R0903

from crispy_forms.layout import Layout, Submit, Div, HTML, Field, Button
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, InlineCheckboxes
from crispy_forms.layout import Submit
from django import forms

from apps.metas.models import Evidencia, MetasSPE, Rol


class EvidenciaForm(forms.ModelForm):

    class Meta:
        model = Evidencia
        exclude = ['campos', ]


class AddRolForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddRolForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('clave', wrapper_class='col-md-2 col-sm-4'),
                Field('description', wrapper_class='col-md-2 col-sm-3'),
                Field('order', wrapper_class='col-md-2 col-sm-3'),
                css_class='row'
            )
        )
        self.helper.add_input(Submit('submit', 'Enviar'))

    class Meta:
        model = Rol
        fields = '__all__'


class MetasSPEForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MetasSPEForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('puesto', wrapper_class='col-md-6 col-sm-8'),
                css_class='row'
            ),
            Div(
                Field('clave', wrapper_class='col-md-2 col-sm-4'),
                Field('nom_corto', wrapper_class='col-md-4 col-sm-8'),
                Field('year', wrapper_class='col-md-2 col-sm-3'),
                Field('ciclos', wrapper_class='col-md-2 col-sm-3'),
                css_class='row'
            ),
            Div(
                Field('description', wrapper_class='col', rows='2'),
                Field('soporte', wrapper_class='col'),
                css_class='row'
            ),
            Div(
                Field('campos', wrapper_class='col', rows='3'),
                css_class='row'
            )
        )
        self.helper.add_input(Submit('submit', 'Enviar'))

    class Meta:
        model = MetasSPE
        fields = '__all__'

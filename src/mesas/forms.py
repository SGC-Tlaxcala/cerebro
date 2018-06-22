# coding: utf-8
#         app: mesa de atención
#      module: forms
#        date: jueves, 14 de junio de 2018 - 08:56
# description: Formulario para la bitácora de ciudadanos rechazados en mac
# pylint: disable=W0613,R0201,R0903

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML, Field, Button
from crispy_forms.bootstrap import FormActions
from django import forms

from mesas.models import Registro


class MesaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MesaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper .layout = Layout(
            Div(
                Field('modulo', wrapper_class='col-md-2', autocomplete='off'),
                Field('fecha', wrapper_class='col-md-2', autocomplete='off'),
                Field('lugar', wrapper_class='col-md-3'),
                css_class='row'
            ),
            Div(
                Field('sexo', wrapper_class='col-md-2'),
                Field('causa', wrapper_class='col-md-3'),
                Field('observaciones', wrapper_class='col-md-6', rows='3'),
                css_class='row'
            ),
            Div(
                HTML('<hr>'),
                FormActions(
                    Submit('save', 'Guardar cambios'),
                    Button('cancel', 'Cancelar')
                )
            )
        )

    class Meta:
        model = Registro
        fields = '__all__'

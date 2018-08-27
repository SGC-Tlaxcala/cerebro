# coding: utf-8
# app: apps.productividad.forms
# date: 26 Aug 2018
# author: Javier Sanchez Toledano <js.toledano@me.com>
"""formulario para subir el archivo de cifras"""

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Div, Field, Button
from crispy_forms.bootstrap import FormActions
from django import forms


class CargaCifras(forms.Form):
    """Clase para crear el formulario que carga las cifras"""
    fecha_corte = forms.DateField(help_text='Escribe la fecha de corte')
    archivo = forms.FileField(help_text='Selecciona el archivo de Excel con la productividad semanal')

    def __init__(self, *args, **kwargs):
        super(CargaCifras, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('fecha_corte', wrapper_class='col-md-2', autocomplete='off'),
                Field('archivo', wrapper_class="col-md-6"),
                css_class='row'
            ),
            Div(
                HTML('<hr>'),
                FormActions(
                    Submit('save', 'Guardar cambios'),
                    Button('cancel', 'Cancelar')
                ),
                css_class='row'
            )
        )

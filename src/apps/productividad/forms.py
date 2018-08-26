# coding: utf-8
# app: apps.productividad.forms
# date: 26 Aug 2018
# author: Javier Sanchez Toledano <js.toledano@me.com>
"""formulario para subir el archivo de cifras"""

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML, Field, Button
from crispy_forms.bootstrap import FormActions
from django import forms


class CargaCifras(forms.Form):
    fecha_corte = forms.DateField()

    def __init__(self, *args, **kwargs):
        super(CargaCifras, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('fecha_corte', wrapper_class='col-md-2', autocomplete='off'),
                css_class='row'
            )

        )

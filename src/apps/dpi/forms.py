# coding: utf-8
"""Formularios para DPI y USI."""

#         app: dpi
#      módulo: forms
# descripción: Formularios para DPI y USI
#       autor: Javier Sanchez Toledano
#       fecha: lunes, 28 de mayo de 2018

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML, Field, Button
from crispy_forms.bootstrap import InlineRadios, Tab, TabHolder, FormActions
from django.core.exceptions import NON_FIELD_ERRORS
from django import forms
from apps.dpi.models import ExpedienteDPI


class ExpedienteForm(forms.ModelForm):
    u"""Formulario automático para expedientes DPI."""

    def __init__(self, *args, **kwargs):
        """Inicializador del formulario."""
        super(ExpedienteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML('<h3>Datos de Identificación</h3>'),
                Div(
                    Field('tipo', wrapper_class='col-sm-4'),
                    Field('folio', wrapper_class='col-sm-3', autocomplete='off'),
                    css_class='row'
                ),
                Div(
                    Field('nombre', wrapper_class='col-md-6', autocomplete='off'),
                    Field('fecha_tramite', wrapper_class='col-sm-3', autocomplete='off'),
                    css_class='row'
                ),
                Div(
                    InlineRadios('estado')
                ),
                HTML('<hr>'),
                Div(
                    Field('tratamiento', wrapper_class='col', autocomplete='off'),
                    Field('captura', wrapper_class='col', autocomplate='off'),
                    css_class='row'
                ),
                Div(
                    Field('atencion', wrapper_class='col', autocomplete='off'),
                    Field('resolucion', wrapper_class='col', autocomplate='off'),
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
            ),
        )

    class Meta:
        """Metadata para expedientes."""

        model = ExpedienteDPI
        fields = '__all__'
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Ya existe un %(model_name)s para esos %(field_labels)s"
            }
        }

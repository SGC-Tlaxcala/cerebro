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
from django import forms
from dpi.models import ExpedienteDPI


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
                TabHolder(
                    Tab('Etapa de Aclaración',
                        Div(
                            Field(
                                'fecha_notificacion_aclaracion',
                                autocomplete='off',
                                wrapper_class='col-xs-2 col-md-3'
                            ),
                            Field('fecha_entrevista', autocomplete='off', wrapper_class='col-xs-2 col-md-3'),
                            Field('fecha_envio_expediente', autocomplete='off', wrapper_class='col-xs-2 col-md-3'),
                            css_class='row'
                        )
                        ),
                    Tab(
                        'Etapa de Validación',
                        Div(
                            Field('fecha_solicitud_cedula', autocomplete='off', wrapper_class='col-xs-2 col-md-3'),
                            Field('fecha_ejecucion_cedula', autocomplete='off', wrapper_class='col-xs-2 col-md-3'),
                            Field('fecha_validacion_expediente', autocomplete='off', wrapper_class='col-xs-2 col-md-3'),
                            css_class='row'
                        )
                    ),
                    Tab('Etapa de notificación de rechazo',
                        Div(
                            Field('fecha_notificacion_rechazo', autocomplete='off', wrapper_class='col-xs-2 col-md-3'),
                            Field(
                                'fecha_notificacion_exclusion',
                                autocomplete='off',
                                wrapper_class='col-xs-2 col-md-3'
                            ),
                            css_class='row'
                            )
                        )
                ),
                Div(
                    FormActions(
                        Submit('save', 'Guardar cambios'),
                        Button('cancel', 'Cancelar')
                    )
                )
            ),
        )

    class Meta:
        """Metadata para expedientes."""

        model = ExpedienteDPI
        fields = '__all__'

# coding: utf-8
"""Formularios para DPI y USI."""

#         app: dpi
#      módulo: forms
# descripción: Formularios para DPI y USI
#       autor: Javier Sanchez Toledano
#       fecha: lunes, 28 de mayo de 2018

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import InlineRadios
from django import forms
from dpi.models import ExpedienteDPI


class ExpedienteForm(forms.ModelForm):
    u"""Formulario automático para expedientes DPI."""

    def __init__(self, *args, **kwargs):
        """Inicializador del formulario."""
        super(ExpedienteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(InlineRadios('estado'),)
        self.helper.add_input(Submit('submit', 'Enviar'))

    class Meta:
        """Metadata para expedientes."""

        model = ExpedienteDPI
        fields = '__all__'

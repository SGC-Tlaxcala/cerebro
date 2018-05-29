# coding: utf-8
"""Formularios para DPI y USI."""

#         app: dpi
#      módulo: forms
# descripción: Formularios para DPI y USI
#       autor: Javier Sanchez Toledano
#       fecha: lunes, 28 de mayo de 2018

from django import forms
from core.utils import HorizontalRadioSelect
from dpi.models import ExpedienteDPI


class ExpedienteForm(forms.ModelForm):
    u"""Formulario automático para expedientes DPI."""

    class Meta:
        """Metadata para expedientes."""

        model = ExpedienteDPI
        fields = '__all__'
        widgets = {
            'estado': HorizontalRadioSelect()
        }

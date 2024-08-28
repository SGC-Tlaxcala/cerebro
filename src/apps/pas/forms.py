# -*- coding: UTF-8 -*-

#         app: Control de Planes de Acción
#      modulo: pas.forms
# descripcion: Formularios
#       autor: Javier Sanchez Toledano
#       fecha: viernes, 3 de octubre de 2014

from .models import Plan
from .models import PROCESO, TIPO, DETECCION, MEJORA
from django import forms
from tinymce.widgets import TinyMCE


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        exclude = []

    fecha_deteccion = forms.DateField(
        input_formats=['%d/%m/%Y', ],
        widget=forms.TextInput(
            attrs={'class': 'form-control', }
        )
    )
    proceso = forms.CharField(
        widget=forms.widgets.Select(
            choices=PROCESO,
            attrs={'class': 'form-control', }
        )
    )
    tipo = forms.CharField(
        widget=forms.widgets.Select(
            choices=TIPO,
            attrs={'class': 'form-control', }
        )
    )
    deteccion = forms.CharField(
        widget=forms.widgets.Select(
            choices=DETECCION,
            attrs={'class': 'form-control', }
        )
    )
    mejora = forms.CharField(
        widget=forms.widgets.Select(
            choices=MEJORA,
            attrs={'class': 'form-control', }
        )
    )

    redaccion = forms.CharField(
        widget=TinyMCE(attrs={'cols': 50, 'rows': 3, 'class': 'form-control'})
    )
    declaracion = forms.CharField(
        widget=TinyMCE(attrs={'cols': 50, 'rows': 3, 'class': 'form-control'})
    )
    evidencia = forms.CharField(
        widget=TinyMCE(attrs={'cols': 50, 'rows': 3, 'class': 'form-control'})
    )
    correccion = forms.CharField(
        widget=TinyMCE(attrs={'cols': 50, 'rows': 3, 'class': 'form-control'})
    )
    causa_raiz = forms.CharField(
        widget=TinyMCE(attrs={'cols': 50, 'rows': 3, 'class': 'form-control'})
    )
    relacionadas = forms.CharField(
        widget=TinyMCE(attrs={'cols': 50, 'rows': 3, 'class': 'form-control'})
    )

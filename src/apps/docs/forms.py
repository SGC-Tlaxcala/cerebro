# coding: utf-8
# Formularios para la app de documentos

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML, Field, Button
from crispy_forms.bootstrap import FormActions
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms

from apps.docs.models import Documento, Proceso, Tipo


class DocForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DocForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('nombre',  wrapper_class='col-md-8', autocomplete='off'),
                css_class='row'
            ),
            Div(
                Field('proceso', wrapper_class='col-md-3', autocomplete='off'),
                Field('tipo', wrapper_class='col-md-3', autocomplete='off'),
                css_class='row'
            ),
            Div(
                Field('texto_ayuda', wrapper_class='col-md-8', rows='3'),
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
        model = Documento
        fields = '__all__'


class ProcesoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProcesoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('proceso', wrapper_class='col-md-12', autocomplete='off'),
                Field('slug', wrapper_class='col-md-12', autocomplete='off'),
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
        model = Proceso
        fields = '__all__'


class TipoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TipoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('tipo', wrapper_class='col-md-12', autocomplete='off'),
                Field('slug', wrapper_class='col-md-12', autocomplete='off'),
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
        model = Tipo
        fields = '__all__'

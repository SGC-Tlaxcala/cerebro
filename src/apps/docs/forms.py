# coding: utf-8
# Formularios para la app de documentos

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML, Field, Button
from crispy_forms.bootstrap import FormActions
from django import forms

from apps.docs.models import Documento, Proceso, Tipo, Revision


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
                ),
                css_class='modal-footer'
            )
        )

    class Meta:
        model = Documento
        fields = ['nombre', 'proceso', 'tipo', 'texto_ayuda']


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


class VersionForm(forms.ModelForm):
    class Meta:
        model = Revision
        fields = ['documento', 'revision', 'f_actualizacion', 'archivo', 'cambios']

    def __init__(self, *args, **kwargs):
        super(VersionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('revision', wrapper_class='col-md-6'),
                Field('f_actualizacion', wrapper_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Field('archivo', wrapper_class='col-md-12'),
                css_class='row'
            ),
            Div(
                Field('cambios', wrapper_class='col', rows=3),
                css_class='row'
            ),
            Div(
                HTML('<hr>'),
                FormActions(
                    Submit('save', 'Guardar cambios')
                )
            )
        )

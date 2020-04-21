# coding: utf-8
# Formularios para la app de documentos

from crispy_forms.layout import Layout, Submit, Div, Field
from crispy_forms.helper import FormHelper
from django import forms
from apps.docs.models import Proceso


class ProcessAddForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProcessAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('proceso', wrapper_class='col-md-6'),
                Field('slug', wrapper_class='col-md-6'),
                css_class='row'
            )
        )
        self.helper.add_input(Submit('submit', 'Enviar'))

    class Meta:
        model = Proceso
        fields = '__all__'

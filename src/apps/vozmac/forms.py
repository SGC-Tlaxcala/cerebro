from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML, Field, Button
from crispy_forms.bootstrap import FormActions
from django import forms


class SurveyBatchForm(forms.Form):
    """Formulario para subir un lote de encuestas."""

    file_name = forms.FileField(
        label='Archivo de encuestas',
        help_text='Seleccione el archivo tar.gz que contiene las encuestas.',
        widget=forms.ClearableFileInput(attrs={'accept': '.gz'})
    )

    def __init__(self, *args, **kwargs):
        """Inicializador del formulario de lote de encuestas."""
        super(SurveyBatchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('file_name', wrapper_class='col-md-8'),
                css_class='row'
            ),
            Div(
                HTML('<hr>'),
                FormActions(
                    Submit('upload', 'Subir Lote'),
                    Button('cancel', 'Cancelar')
                ),
                css_class='modal-footer'
            )
        )

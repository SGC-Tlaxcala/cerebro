from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
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
        self.fields['file_name'].widget.attrs.update(
            {
                'class': 'file-input file-input-bordered w-full max-w-lg',
            }
        )

        self.helper = FormHelper()
        self.helper.template_pack = 'tailwind'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Field('file_name', wrapper_class='flex flex-col gap-2'),
                css_class='w-full'
            )
        )

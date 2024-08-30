from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Column, Row, Div, HTML
from crispy_forms.bootstrap import Tab, TabHolder, FormActions, InlineRadios, Field
from .models import Plan


class PlanForm(forms.ModelForm):

    # el campo otra_fuente está disabled por defecto
    # para habilitarlo se debe seleccionar la opción
    # Otros en el campo fuente
    otra_fuente = forms.CharField(
        label='Otra fuente',
        required=False,
        widget=forms.TextInput(attrs={'disabled': 'disabled'})
    )

    class Meta:
        model = Plan
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(PlanForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                HTML('<h3>Identificación del plan</h3>'),
                Row(Column('nombre', wrapper_class='mb-3 col-sm-12')),
                Row(
                    Column('documento'),
                    Column('fecha_llenado'),
                    Column('folio'),
                ),
                Row(
                    Div(
                        HTML('<h2>Descripción de la No Conformidad / Riesgo</h2>'),
                        Row(Column('tipo'), Column('fuente')),
                        Row(Column('otra_fuente')),
                        Row(Column('desc_cnc'), Column('correccion')),
                        css_class='h-100 p-5 bg-body-tertiary border rounded-3',
                        css_id='descripcion_cnc'
                    ),
                    css_class='mb-3'
                ),
                Row(
                    Div(
                        HTML('<h2>Descripción del Plan de Cambios y Mejoras al SGC</h2>'),
                        Row(Column('fecha_inicio'), Column('fecha_termino'), Column('requisito')),
                        Row(Column('proposito'), Column('proceso')),
                        Row(Column('desc_pcm'), Column('consecuencias')),
                        css_class='h-100 p-5 bg-body-tertiary border rounded-3',
                        css_id='descripcion_pcm'
                    ),
                    css_class='mb-3'
                ),
            ),
            ButtonHolder(
                Submit('submit', 'Guardar')
            )
        )

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Column, Row, Div, HTML, Button
from crispy_forms.bootstrap import Tab, TabHolder, FormActions
from .models import Plan


class PlanForm(forms.ModelForm):

    otra_fuente = forms.CharField(
        label='Otra fuente',
        required=False,
        widget=forms.TextInput(attrs={'disabled': 'disabled'})
    )

    class Meta:
        model = Plan
        exclude = ['user']

    def clean(self):
        cleaned_data = super(PlanForm, self).clean()
        fuente = cleaned_data.get('fuente')
        otra_fuente = cleaned_data.get('otra_fuente')
        if fuente == 4 and not otra_fuente:
            self.add_error('otra_fuente', 'Este campo es obligatorio si seleccionó Otros')
        return cleaned_data

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
                Row(
                    TabHolder(
                        Tab('Análisis de la Causa Raíz'),
                        Tab('Actividades'),
                        Tab('Seguimiento'),
                        Tab('Cierre'),
                        css_class='mt-3 mb-3'
                    ),
                    css_class='mb-4',
                    css_id='tabs'
                )
            ),
            FormActions(
                Submit('submit', 'Guardar'),
                Button('cancel', 'Cancelar', css_class='btn btn-danger', onclick='window.history.back()')
            )
        )

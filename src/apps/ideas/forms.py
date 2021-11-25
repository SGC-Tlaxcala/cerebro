# coding: utf-8
"""Formularios para agregar una idea o proyecto."""

#         app: ideas
#      módulo: forms
# descripción: Formularios para agregar una idea o proyecto.
#       autor: Javier Sanchez Toledano
#       fecha: lunes, 25 de noviembre de 2021

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML, Field, Button
from crispy_forms.bootstrap import InlineRadios, Tab, TabHolder, FormActions
from django.core.exceptions import NON_FIELD_ERRORS
from django import forms
from .models import Idea


class IdeaForm(forms.ModelForm):

    class Meta:
        model = Idea
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super(IdeaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML('<h3>Déjanos tus datos</h3>'),
                Div(
                    Field('name', wrapper_class='col-sm-12'),
                    Field('contacto', wrapper_class='col-sm-3', autocomplete='off'),
                    css_class='row'
                ),
                Div(
                    Field('contact', wrapper_class='col'),
                    Field('site', wrapper_class='col'),
                    css_class='row'
                ),
                HTML('<hr>'),
                HTML('<h3>Cuéntanos tu idea</h3>'),
                Div(
                    Field('type', wrapper_class='col-md-3'),
                    Field('scope', wrapper_class='col-md-3'),
                    css_class='row'
                ),
                Div(
                    Field('desc', wrapper_class='col-md-7', rows='5'),
                    HTML('''
                        <p class="text-muted col-md-5">
                        Describe tu <strong>idea</strong>. Qué te gustaría que cambiara en el SGC Tlaxcala
                        para mejorar. Tu idea puede impactar a un proceso, una actividad, un objetivo o
                        un indicador. <br><br>
                        ¿Sugieres agregar un formato para mejorar el control de un proceso? ¿Quitar otro para
                        hacer una actividad más ágil? ¿Cambiar un indicador para que sea más preciso?
                        <strong>¡Tus ideas son bienvenidas!</strong><br><br><br>

                        Elige <strong>proyecto</strong> si ya estás llevando a cabo tu idea.<br>
                        Recuerda que un <em>proyecto</em> tiene un término y un objetivo claro. Al final
                        debes indicar el grado en el que cumpliste ese objetivo.
                    </p>'''),
                    css_class='row'
                ),
                HTML('<hr>'),
                Div(
                    HTML('''<p class="lead col">
                    Si estás ejecutando un proyecto actualmente o este ya terminó, comparte
                    los resultados que esperas obtener o que has obtenido hasta la fecha.
                    <p>'''),
                    css_class='row'
                ),
                Div(
                    Field('results', wrapper_class='col-md-7', rows='5'),
                    Div(
                      Field('docs', wrapper_class='col-md-12'),
                      Field('evidence', wrapper_class='col-md-12'),
                      css_class='col-md-5',
                    ),
                    css_class='row'
                ),
                Div(
                    HTML('<hr>'),
                    FormActions(
                        Submit('save', 'Guardar cambios'),
                        Button('cancel', 'Cancelar')
                    ),
                    css_class='row'
                )
            ),
        )




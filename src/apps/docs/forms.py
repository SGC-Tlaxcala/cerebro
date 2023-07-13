"""
Clases forms.py.

Gestiona las clases y funciones de los formularios de la documentación.
"""

# Formularios para la app de documentos

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML, Field, Button
from crispy_forms.bootstrap import FormActions
from django import forms

from apps.docs.models import Documento, Proceso, Tipo, Revision

GUARDAR_CAMBIOS = 'Guardar cambios'


class DocForm(forms.ModelForm):
    """Formulario para crear un documento nuevo."""

    def __init__(self, *args, **kwargs):
        """Inicialización del formulario de documentos."""
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
                    Submit('save', GUARDAR_CAMBIOS),
                    Button('cancel', 'Cancelar')
                ),
                css_class='modal-footer'
            )
        )

    class Meta:
        """Metadata de la clase DocForm."""

        model = Documento
        fields = ['nombre', 'proceso', 'tipo', 'texto_ayuda']


class ProcesoForm(forms.ModelForm):
    """
    Clase ProcesoForm.

    Formulario simple para crear  un nuevo tipo de proceso.
    """

    def __init__(self, *args, **kwargs):
        """Inicializador del formulario de procesos."""
        super(ProcesoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field(
                    'proceso',
                    wrapper_class='col-md-12',
                    autocomplete='off'),
                Field('slug', wrapper_class='col-md-12', autocomplete='off'),
                css_class='row'
            ),
            Div(
                HTML('<hr>'),
                FormActions(
                    Submit('save', GUARDAR_CAMBIOS),
                    Button('cancel', 'Cancelar')
                )
            )
        )

    class Meta:
        """Metadatos de la clase ProcesoForm."""

        model = Proceso
        fields = ['proceso', 'slug']


class TipoForm(forms.ModelForm):
    """
    Clase TipoForm.

    Formulario simple para crear un nuevo tipo de documento.
    """

    def __init__(self, *args, **kwargs):
        """Inicializador para la clase TipoForm."""
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
                    Submit('save', GUARDAR_CAMBIOS),
                    Button('cancel', 'Cancelar')
                )
            )
        )

    class Meta:
        """Metadatos de la clase TipoForm."""

        model = Tipo
        fields = ['tipo', 'slug']


class VersionForm(forms.ModelForm):
    """
    Clase VersionForm.

    Crea una nueva versión del documento dado. Ofrece como sugerencia
    el siguiente número de versión y la fecha actual como fecha de
    actualización.

    Argumentos:
      - doc: Identificador del documento.
    """

    class Meta:
        """Metadatos de VersionForm."""

        model = Revision
        fields = [
            'documento',
            'revision',
            'f_actualizacion',
            'archivo',
            'cambios'
        ]

    def __init__(self, *args, **kwargs):
        """Inicializador de la clase VersionForm."""
        super(VersionForm, self).__init__(*args, **kwargs)
        self.fields['f_actualizacion'].label = "Fecha de Actualización"
        # Prefill the revision field with the next revision number
        self.fields['revision'].text = self.instance

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('revision', wrapper_class='col-md-6'),
                Field('f_actualizacion', wrapper_class='col-md-6', attrs={
                    "label": "Fecha de Actualización"
                }),
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
                    Submit('save', GUARDAR_CAMBIOS)
                )
            )
        )

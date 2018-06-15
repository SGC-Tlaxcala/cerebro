# coding: utf-8
# Formularios para la app de documentos

from django import forms
from docs.models import Documento
from docs.models import Revision


class DocumentoForm (forms.ModelForm):
    class Meta:
        model = Documento
        exclude = ('slug',)
        f_actualizacion = forms.DateField(
        widget=BootstrapDateInput(
            attrs={},
        ), ) 


class RevisionForm (forms.ModelForm):
    class Meta:
        model = Revision
    f_actualizacion = forms.DateField(
        widget=BootstrapDateInput(
            attrs={},
        ), )
    cambios = forms.CharField(
                label = 'Registro de Cambios',
                widget=forms.Textarea(
                    attrs={
                          'rows':5
                        , 'cols': 78
                        , 'style':'width: 80%; height: 120px'
                        , 'class':'wmd-input'
                    }
                )
            )    
    revision = forms.CharField ( widget=BootstrapTextInput( attrs={'class':'input-mini',}, ), )

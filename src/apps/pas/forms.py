from django import forms
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


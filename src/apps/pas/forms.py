from django import forms
from django.forms import (
    TextInput,
    NumberInput,
    EmailInput,
    DateInput,
    TimeInput,
    URLInput,
    Select,
    SelectMultiple,
    Textarea,
    CheckboxInput,
    ClearableFileInput,
)
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
        widget_class_map = {
            TextInput: 'input input-bordered w-full',
            NumberInput: 'input input-bordered w-full',
            EmailInput: 'input input-bordered w-full',
            DateInput: 'input input-bordered w-full',
            TimeInput: 'input input-bordered w-full',
            URLInput: 'input input-bordered w-full',
            Select: 'select select-bordered w-full',
            SelectMultiple: 'select select-bordered w-full',
            Textarea: 'textarea textarea-bordered w-full min-h-[160px]',
            CheckboxInput: 'toggle toggle-primary',
            ClearableFileInput: 'file-input file-input-bordered w-full',
        }

        for name, field in self.fields.items():
            widget = field.widget
            for widget_type, css_class in widget_class_map.items():
                if isinstance(widget, widget_type):
                    existing = widget.attrs.get('class', '')
                    widget.attrs['class'] = f'{existing} {css_class}'.strip()
                    break

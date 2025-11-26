from django import forms

from .models import Idea


INPUT_CLASSES = 'input input-bordered w-full'
SELECT_CLASSES = 'select select-bordered w-full'
TEXTAREA_CLASSES = 'textarea textarea-bordered w-full min-h-[160px]'
FILE_CLASSES = 'file-input file-input-bordered w-full'


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = (
            'name',
            'contact',
            'site',
            'title',
            'type',
            'scope',
            'desc',
            'results',
            'docs',
            'evidence',
        )
        widgets = {
            'desc': forms.Textarea(attrs={'rows': 6}),
            'results': forms.Textarea(attrs={'rows': 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.Textarea):
                widget.attrs.setdefault('class', TEXTAREA_CLASSES)
            elif isinstance(widget, forms.Select):
                widget.attrs.setdefault('class', SELECT_CLASSES)
            elif isinstance(widget, forms.FileInput):
                widget.attrs.setdefault('class', FILE_CLASSES)
            else:
                widget.attrs.setdefault('class', INPUT_CLASSES)
            widget.attrs.setdefault('placeholder', field.label)
        self.fields['contact'].widget.attrs.setdefault('type', 'email')
        self.fields['contact'].widget.attrs.setdefault('autocomplete', 'email')

    def clean_contact(self):
        contact = self.cleaned_data.get('contact', '')
        if '@ine.mx' not in contact:
            raise forms.ValidationError('El contacto debe ser un correo institucional válido.')
        return contact


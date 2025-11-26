from django import forms
from django.contrib.auth import get_user_model

from apps.profiles.api.serializers import UserProfileSerializer
from .models import ENTIDADES, SITIO, PUESTOS, TLAXCALA, RA


User = get_user_model()


WIDGET_CLASS_MAP = {
    forms.TextInput: 'input input-bordered w-full',
    forms.EmailInput: 'input input-bordered w-full',
    forms.PasswordInput: 'input input-bordered w-full',
    forms.Select: 'select select-bordered w-full',
    forms.Textarea: 'textarea textarea-bordered w-full',
    forms.CheckboxInput: 'toggle toggle-primary',
}


def apply_tailwind_widgets(form):
    for field in form.fields.values():
        widget = field.widget
        for widget_type, css in WIDGET_CLASS_MAP.items():
            if isinstance(widget, widget_type):
                existing = widget.attrs.get('class', '')
                widget.attrs['class'] = f'{existing} {css}'.strip()
                break


class QuickUserProfileForm(forms.ModelForm):
    password = forms.CharField(
        label='Contraseña temporal',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        required=False,
        help_text='Si se deja en blanco, se generará automáticamente.',
    )
    state = forms.TypedChoiceField(label='Entidad', choices=ENTIDADES, initial=TLAXCALA, coerce=int)
    site = forms.TypedChoiceField(label='Sede', choices=SITIO, initial=0, coerce=int)
    position = forms.ChoiceField(label='Puesto', choices=PUESTOS, initial=RA)
    recibe_notificaciones = forms.BooleanField(
        label='Recibe notificaciones',
        required=False,
        initial=False,
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        labels = {
            'first_name': 'Nombre(s)',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'username': 'Usuario',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_tailwind_widgets(self)
        email_field = self.fields['email']
        email_field.required = True
        email_field.widget.input_type = 'email'
        self.fields['username'].help_text = 'Se usará el correo si se deja vacío.'
        self._generated_password = None

    def clean_username(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if not username:
            if not email:
                raise forms.ValidationError('Debe proporcionar un usuario o correo.')
            username = email
        return username

    def save(self, commit=True):
        data = self.cleaned_data
        password = data.get('password') or User.objects.make_random_password()
        payload = {
            'username': data.get('username') or data.get('email'),
            'first_name': data.get('first_name', ''),
            'last_name': data.get('last_name', ''),
            'email': data.get('email'),
            'password': password,
            'is_active': True,
            'profile': {
                'state': data.get('state', TLAXCALA),
                'site': data.get('site', 0),
                'position': data.get('position', RA),
                'recibe_notificaciones': data.get('recibe_notificaciones', False),
            },
        }
        serializer = UserProfileSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self._generated_password = password
        return user

    @property
    def generated_password(self):
        return self._generated_password

    @staticmethod
    def display_name(user):
        full_name = (user.get_full_name() or '').strip()
        if full_name:
            return full_name
        return user.email or user.username

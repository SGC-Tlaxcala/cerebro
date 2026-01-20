from django import forms
from .models import Subscriber


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["nombre_completo", "usuario_inst"]
        labels = {
            "nombre_completo": "Nombre Completo",
            "usuario_inst": "Usuario Institucional",
        }
        help_texts = {
            "usuario_inst": "Ingresa solo tu nombre de usuario (ej. javier.sanchezt).",
        }

    def clean_usuario_inst(self):
        usuario = self.cleaned_data["usuario_inst"].lower().strip()
        if "@" in usuario:
            # Si el usuario ingresó correo, limpiamos
            usuario = usuario.split("@")[0]
        return usuario

import uuid
from django.db import models


class Subscriber(models.Model):
    nombre_completo = models.CharField(max_length=255)
    usuario_inst = models.CharField(
        max_length=150,
        unique=True,
        help_text="Usuario institucional (ej. javier.sanchezt)",
    )
    is_active = models.BooleanField(default=False)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario_inst

    @property
    def email_full(self):
        return f"{self.usuario_inst}@ine.mx"

from django.db import models


class PaqueteEncuesta(models.Model):
    """
    Registra cada archivo JSON subido desde un MAC.
    Actúa como un control para evitar procesar el mismo archivo dos veces.
    """
    file_name = models.CharField(max_length=100, unique=True,
                                 help_text="Nombre del archivo original, ej: 290151A_20251015_093000.json.gz")
    file_hash = models.CharField(max_length=64, unique=True,
                                 help_text="Hash SHA-256 del contenido del archivo para asegurar unicidad.")
    mac = models.CharField(max_length=6, help_text="MAC extraída del nombre del archivo.")
    device_id = models.CharField(max_length=1, help_text="ID del dispositivo extraído del nombre del archivo.")
    record_count = models.PositiveIntegerField(default=0, help_text="Número de encuestas contenidas en este archivo.")
    uploaded_at = models.DateTimeField(auto_now_add=True,
                                       help_text="Fecha y hora en que se subió el archivo al sistema.")

    def __str__(self):
        return self.file_name


class RespuestaEncuesta(models.Model):
    batch = models.ForeignKey(PaqueteEncuesta, on_delete=models.CASCADE, related_name="responses")

    entidad = models.PositiveSmallIntegerField(default=29, editable=False)
    distrito = models.PositiveSmallIntegerField(editable=False)
    mac = models.CharField(max_length=6, editable=False)

    device_id = models.CharField(max_length=8)
    p0_tipo_visita = models.PositiveSmallIntegerField()
    p1_claridad_info = models.PositiveSmallIntegerField()
    p2_amabilidad = models.PositiveSmallIntegerField()
    p3_instalaciones = models.PositiveSmallIntegerField()
    p4_tiempo_espera = models.PositiveSmallIntegerField()
    is_exported = models.BooleanField(default=False)
    created_at = models.DateTimeField(help_text="Fecha y hora de la encuesta en el dispositivo")

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Extrae sólo dígitos del device_id
        if self.device_id:
            digits = ''.join(ch for ch in self.device_id if ch.isdigit())
            # entidad: primeros 2 dígitos
            if len(digits) >= 2:
                try:
                    self.entidad = int(digits[0:2])
                except ValueError:
                    pass
            # distrito: dígitos 3 y 4 (índices 2:4)
            if len(digits) >= 4:
                try:
                    self.distrito = int(digits[2:4])
                except ValueError:
                    pass
            # mac: primeros 6 dígitos (o lo que haya hasta 6)
            if len(digits) >= 1:
                self.mac = digits[:6] if len(digits) >= 6 else digits

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Encuesta del {self.created_at.strftime('%Y-%m-%d')}"

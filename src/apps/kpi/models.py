"""
Este archivo define los modelos relacionados con las campañas y los trámites mensuales en el sistema KPI.

Clases:
- Campaign: Representa una campaña anual, ya sea permanente o intensa, con sus metas y acumulados.
- TramiteMensual: Representa los trámites realizados en un mes específico dentro de una campaña.

Detalles:
- Campaign incluye métodos para calcular el acumulado basado en los trámites mensuales registrados.
- TramiteMensual valida que los meses correspondan al tipo de campaña antes de guardar los datos.

Dependencias:
- models: Proporciona las clases base para definir modelos en Django.
- ValidationError: Permite manejar errores de validación personalizados.
"""
from django.db import models
from django.core.exceptions import ValidationError


class Campaign(models.Model):
    """
    Modelo Campaign.

    Representa una campaña anual en el sistema KPI, que puede ser permanente o intensa.
    Campos:
    - year: Año de la campaña.
    - type: Tipo de campaña ('CAP' para Campaña Anual Permanente, 'CAI' para Campaña Anual Intensa).
    - meta: Meta establecida para la campaña.
    - forecast: Pronóstico de trámites esperados.
    - acumulado: Porcentaje acumulado de trámites realizados.

    Métodos:
    - update_acumulado: Recalcula el porcentaje acumulado basado en los trámites mensuales registrados.

    Meta:
    - unique_together: Garantiza que no existan dos campañas con el mismo año y tipo.
    """
    CAP = 'CAP'
    CAI = 'CAI'
    TYPE_CHOICES = [
        (CAP, 'Campaña Anual Permanente'),
        (CAI, 'Campaña Anual Intensa'),
    ]

    year = models.PositiveIntegerField()
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    meta = models.DecimalField(max_digits=5, decimal_places=2)
    forecast = models.PositiveIntegerField('Pronóstico de trámites esperados')
    acumulado = models.PositiveIntegerField('Trámites acumulados', default=0,
                                            editable=False, help_text='Número de trámites acumulados hasta la fecha')
    avance = models.FloatField(default=0.0, editable=False, help_text='Porcentaje de avance de la campaña')

    class Meta:
        unique_together = ('year', 'type')
        verbose_name = 'Campaña'
        verbose_name_plural = 'Campañas'

    def __str__(self):
        return f"{self.get_type_display()} {self.year}"

    def update_acumulado(self):
        """
        Recalcula el acumulado y el avance de la campaña basado en los trámites mensuales registrados.
        """
        total = self.tramitemensual_set.aggregate(
            total=models.Sum('tramites')
        )['total'] or 0

        avance = (total / self.forecast) * 100 if self.forecast else 0

        # Solo actualiza si hay cambios
        if self.acumulado != total or self.avance != avance:
            self.acumulado = total
            self.avance = avance
            self.save(update_fields=['acumulado', 'avance'])


class TramiteMensual(models.Model):
    """
    Modelo TramiteMensual.

    Representa los trámites realizados en un mes específico dentro de una campaña.
    Campos:
    - campaign: Relación con la campaña asociada.
    - year: Año en el que se realizaron los trámites.
    - month: Mes en el que se realizaron los trámites (1 para enero, 12 para diciembre).
    - tramites: Número total de trámites realizados en el mes.

    Métodos:
    - clean: Valida que el mes corresponda al tipo de campaña antes de guardar.
    - save: Ejecuta la validación y actualiza el acumulado de la campaña asociada.

    Meta:
    - unique_together: Garantiza que no existan registros duplicados para la misma campaña, año y mes.
    """
    MONTH_CHOICES = [(i, i) for i in range(1, 13)]

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    month = models.PositiveSmallIntegerField(choices=MONTH_CHOICES)
    tramites = models.PositiveIntegerField()

    class Meta:
        unique_together = ('campaign', 'month')
        verbose_name = 'Trámites'

    def __str__(self):
        return f"{self.campaign} - {self.month:02d}"

    def clean(self):
        """
        Valida que el mes corresponda al tipo de campaña.
        """
        if self.campaign.type == Campaign.CAP and not (1 <= self.month <= 8):
            raise ValidationError('CAP solo permite meses de enero a agosto.')
        if self.campaign.type == Campaign.CAI and not (9 <= self.month <= 12):
            raise ValidationError('CAI solo permite meses de septiembre a diciembre.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Ejecuta la validación antes de guardar
        super().save(*args, **kwargs)
        self.campaign.update_acumulado()

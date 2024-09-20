from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum
from apps.pas.models import TrackingFields

User = get_user_model()

KPO = 1
KPI = 2
TYPE = (
    (KPO, 'Objetivo'),
    (KPI, 'Indicador')
)

# Definition of constant of PERIODS of time
PERIODS = (
    (1, 'Semanal'),
    (1, 'Remesa'),
    (3, 'Mensual'),
    (4, 'Bimestral'),
    (5, 'Trimestral'),
    (6, 'Cuatrimestral'),
    (7, 'Semestral'),
    (8, 'Anual'),
    (9, 'Por campaña'),
    (10, 'Por campaña/remesa'),
    (11, 'Por campaña/mensual'),
    (12, 'Por campaña/semanal'),
)


class KPI(TrackingFields):
    pos = models.IntegerField('Posición', help_text='Posición u orden del Indicador')
    type = models.IntegerField('Tipo', choices=TYPE, help_text='Indica si es una Objetivo o un KPI')
    name = models.CharField('Nombre', max_length=255, help_text='Nombre del Objetivo o Indicador')
    description = models.TextField('Descripción', help_text='Descripción detallada del Objetivo o Indicador')
    formula = models.TextField('Fórmula')
    lapse = models.IntegerField('Medición', choices=PERIODS, help_text='Periodo de medición', default=3)
    active = models.BooleanField('Activo', default=True)

    class Meta:
        verbose_name = 'Indicador'
        verbose_name_plural = 'Indicadores'

    def __str__(self) -> str:
        return f'{self.get_type_display()}: {self.name}'


class Period(models.Model):
    """Model to store the periods of the KPIs."""
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE)
    period = models.CharField('Periodo', max_length=255, help_text='Descripción o nombre del periodo de tiempo')
    start = models.DateField('Inicio', help_text='Fecha de inicio del periodo')
    end = models.DateField('Fin', help_text='Fecha de fin del periodo')
    target = models.FloatField('Meta')
    nominal = models.FloatField('Nominativo')
    active = models.BooleanField('Activo', default=True)

    class Meta:
        verbose_name = 'Periodo'
        verbose_name_plural = 'Periodos'
        ordering = ('kpi', 'period',)

    def __str__(self) -> str:
        return f'{self.kpi.name} - {self.period}: {self.target}'

    @property
    def total(self):
        return self.record_set.aggregate(total=models.Sum('value'))['total'] or 0

    @property
    def percent(self):
        return self.total / self.nominal * 100 if self.target else 0


class Record(TrackingFields):
    """Model to store the records of the KPIs."""
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    date = models.DateField('Fecha')
    value = models.FloatField('Valor')
    cumulative_value = models.FloatField('Valor Acumulado', default=0)

    class Meta:
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'
        ordering = ('period__kpi', 'date',)

    def __str__(self) -> str:
        return f'{self.period.kpi.name} - {self.date}: {self.value}'

    def save(self, *args, **kwargs):
        # Calculate the cumulative value
        previous_records = Record.objects.filter(period=self.period, date__lte=self.date).exclude(pk=self.pk)
        self.cumulative_value = previous_records.aggregate(total=Sum('value'))['total'] or 0
        self.cumulative_value += self.value
        super().save(*args, **kwargs)

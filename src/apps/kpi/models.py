from django.contrib.auth import get_user_model
from django.db import models
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
    ('1', 'Semanal'),
    ('2', 'Remesa'),
    ('3', 'Mensual'),
    ('4', 'Bimestral'),
    ('5', 'Trimestral'),
    ('6', 'Cuatrimestral'),
    ('7', 'Semestral'),
    ('8', 'Anual'),
    ('C', 'Por campaña'),
    ('R', 'Por campaña/remesa'),
    ('M', 'Por campaña/mensual'),
    ('S', 'Por campaña/semanal'),
)


class KPI(TrackingFields):
    pos = models.IntegerField('Posición', help_text='Posición u orden del Indicador')
    type = models.IntegerField('Tipo', choices=TYPE, help_text='Indica si es una Objetivo o un KPI')
    name = models.CharField('Nombre', max_length=255, help_text='Nombre del Objetivo o Indicador')
    description = models.TextField('Descripción', help_text='Descripción detallada del Objetivo o Indicador')
    formula = models.TextField('Fórmula')
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


class Record(TrackingFields):
    """Model to store the records of the KPIs."""
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    date = models.DateField('Fecha')
    value = models.FloatField('Valor')

    class Meta:
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'
        ordering = ('period__kpi', 'date',)

    def __str__(self) -> str:
        return f'{self.period.kpi.name} - {self.date}: {self.value}'

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
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
    """Model to store Key Performance Objectives (KPOs) & Indicators (KPIs).

    Attributes:
        pos (int): Position or order of the KPI.
        type (int): Type of the KPI, chosen from predefined types (KPO or KPI).
        name (str): Name of the KPI.
        description (str): Detailed description of the KPI.
        period (int): Period of time for the KPI, chosen from predefined periods.
        period_begin (date): Start date of the KPI period.
        period_end (date): End date of the KPI period.
        formula (str): Formula used to calculate the KPI.
        target (float): Target value for the KPI.
        nominal (float): Nominal value for the KPI.
        active (bool): Indicates if the KPI is active.
        created_at (datetime): Timestamp when the KPI was created.
        updated_at (datetime): Timestamp when the KPI was last updated.
        user (User): User who created the KPI.
    """

    # Identification
    pos = models.IntegerField('Posición', help_text='Posición u orden del Indicador')
    type = models.IntegerField('Tipo', choices=TYPE, help_text='Indica si es una Objetivo o un KPI')
    name = models.CharField('Nombre', max_length=255, help_text='Nombre del Objetivo o Indicador')
    description = models.TextField('Descripción', help_text='Descripción detallada del Objetivo o Indicador')

    # Period of time
    period = models.CharField('Periodo', max_length=1, choices=PERIODS, help_text='Periodo de medición del Indicador')
    period_begin = models.DateField('Inicio')
    period_end = models.DateField('Fin')
    lapse = models.CharField('Lapso', max_length=255, blank=True, null=True, editable=False)

    # Values and results
    formula = models.TextField('Fórmula')
    target = models.FloatField('Meta')
    nominal = models.FloatField('Nominativo')

    active = models.BooleanField('Activo', default=True)

    class Meta:
        verbose_name = 'Indicador'
        verbose_name_plural = 'Indicadores'

    def save(self, *args, **kwargs) -> None:
        """Actividades antes de ejecutar save."""
        self.lapse = f'{self.period_end.year}' if self.period_begin.year == self.period_end.year else f'{self.period_begin.year} - {self.period_end.year}'
        super(KPI, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.get_type_display()}: {self.name} - {self.lapse}'


class Record(TrackingFields):
    """Model to store the records of the KPIs."""
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE)
    date = models.DateField('Fecha')
    value = models.FloatField('Valor')

    class Meta:
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'
        ordering = ('kpi', 'date',)

    def __str__(self) -> str:
        return f'{self.kpi.name} - {self.date}: {self.value}'

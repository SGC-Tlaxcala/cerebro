from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

KPO = 1
KPI = 2
TYPE = (
    (KPO, 'KPO'),
    (KPI, 'KPI')
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
    ('99', 'Por campaña')
)


class KPI(models.Model):
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
    pos = models.IntegerField('Posición', help_text='Posición u orden del KPI')
    type = models.IntegerField('Tipo', choices=TYPE, help_text='Indica si es una KPO o un KPI')
    name = models.CharField('Nombre', max_length=255, help_text='Nombre del KPI o KPO')
    description = models.TextField('Descripción', help_text='Descripción detallada del KPI o KPO')

    # Period of time
    period = models.IntegerField('Periodo', choices=PERIODS)
    period_begin = models.DateField('Inicio')
    period_end = models.DateField('Fin')
    lapse = models.CharField('Lapso', max_length=255, blank=True, null=True, editable=False)

    # Values and results
    formula = models.TextField('Fórmula')
    target = models.FloatField('Meta')
    nominal = models.FloatField('Nominativo')

    active = models.BooleanField('Activo', default=True)

    # Traceability
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Indicador'
        verbose_name_plural = 'Indicadores'

    def save(self, *args, **kwargs) -> None:
        """Actividades antes de ejecutar save."""
        self.lapse = f'{self.period_end.year}' if self.period_begin.year == self.period_end.year else f'{self.period_begin.year} - {self.period_end.year}'
        super(KPI, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.name} - {self.lapse}'

# coding: utf-8
#         app: productividad
#      module: modelos
#        date: viernes, 29 de junio de 2018 - 09:23
# description:
# pylint: disable=W0613,R0201,R0903


import uuid

from django.conf import settings
from django.db import models

from apps.commons.modulos import Modulo

B = 1
B1 = 2
B2 = 3
B3 = 4
B4 = 5

ESTACIONES = (
    (B, 'Básico'),
    (B1, 'Básico + 1'),
    (B2, 'Básico + 2'),
    (B3, 'Básico + 3'),
    (B4, 'Básico + 4')
)

FIJO = 1
FIJO_ADICIONAL = 2
SEMIFIJO = 3
MOVIL = 4

TIPO_MAC = (
    (FIJO, 'Fijo Distrital'),
    (FIJO_ADICIONAL, 'Fijo Adicional'),
    (SEMIFIJO, 'Semifijo'),
    (MOVIL, 'Móvil')
)


class ReporteSemanal(models.Model):
    """Modelo de registro de Reporte Semanal."""
    # Datos del reporte
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # pylint: disable=invalid-name
    fecha_corte = models.DateField('Fecha de Corte')
    remesa = models.CharField('Remesa', max_length=7, unique=True)
    notas = models.TextField('Observaciones')

    # Datos de identificación y seguimiento
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='productividad_remesa',
        on_delete=models.CASCADE,
        editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Remesa %s' % self.remesa

    class Meta:
        """Metadatos de ReporteSemanal."""
        verbose_name = "Reporte de Productividad"
        verbose_name_plural = "Reportes de Productividad"
        ordering = ["-fecha_corte"]
        get_latest_by = 'fecha_corte'


class Cifras(models.Model):
    """Modelo para cifras."""

    # Datos del indicador
    reporte_semanal = models.ForeignKey(ReporteSemanal, on_delete=models.CASCADE,)

    # Datos del Módulo
    modulo = models.ForeignKey(Modulo, related_name='cifras_semanales', on_delete=models.CASCADE,)

    # Datos de productividad
    tramites = models.IntegerField()
    cred_recibidas = models.IntegerField('Credenciales recibidas')
    cred_entregadas = models.IntegerField('Credenciales entregadas')

    # Datos calculados
    atenciones = models.IntegerField(editable=False)
    prod_dia = models.DecimalField(decimal_places=2, max_digits=10, editable=False)
    prod_dia_est = models.DecimalField(decimal_places=2, max_digits=10, editable=False)

    # Datos de trabajo
    dias_trabajados = models.PositiveSmallIntegerField('Días trabajados')
    jornada = models.DecimalField("Jornada Trabajada", decimal_places=2, max_digits=5, null=True)

    # Datos de identificación y seguimiento
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='productividad_cifras',
        on_delete=models.CASCADE,
        editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s - %s" % (self.mac, self.reporte_semanal)

    def save(self, *args, **kwargs):
        self.atenciones = self.tramites + self.cred_entregadas
        self.prod_dia = (self.tramites + self.cred_entregadas) / self.jornada
        self.prod_dia_est = (
                (self.tramites + self.cred_entregadas) / self.jornada
            ) / self.mac.historialmodulo.last().estaciones
        super(Cifras, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Cifras Semanales"
        verbose_name_plural = "Reportes de Cifras"
        ordering = ["mac__distrito", "mac__mac"]

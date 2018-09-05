# coding: utf-8
"""Modelos para depuración"""
#         app: DPI
#      module: Modelos para DPI y USI
#        date: lunes, 28 de mayo de 2018 - 12:30
# description: Modelos para capturar la información sobre DPI y USI
# pylint: disable=W0613,R0201,R0903


import uuid

from django.contrib.auth.models import User
from django.db import models

from core.models import TimeStampedModel
from core.utils import delta

DPI = 'DPI'
USI = 'USI'
TIPOS = (
    (DPI, 'Datos Personales Irregulares'),
    (USI, 'Usurpación de Identidad')
)
NO_INDICA = 0
RECHAZADO = 1
ERROR_MAC = 2
ACLARADO = 3
ESTADO = (
    (NO_INDICA, 'No indica'),
    (RECHAZADO, 'Rechazado'),
    (ERROR_MAC, 'Error en MAC'),
    (ACLARADO, 'Aclarado')
)


class ExpedienteDPI(TimeStampedModel):
    """modelo de expediente"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo = models.CharField(choices=TIPOS, max_length=3)
    folio = models.CharField(max_length=13)
    nombre = models.CharField(max_length=100)

    # Etapa de VRD
    fecha_tramite = models.DateField(null=True, blank=True)

    tratamiento = models.DateField(help_text="Enviado a tratamiento de análisis registral")
    captura = models.DateField(help_text="Situación en proceso de captura")
    atencion = models.DateField(help_text="Pendiente de atención en la Vocalía Local")
    resolucion = models.DateField(help_text="Pendiente de resolución en análisis registral")

    # Cálculo de intervalos de tiempo
    entidad = models.PositiveSmallIntegerField(
        help_text='Entidad',
        editable=False
    )
    distrito = models.PositiveSmallIntegerField(
        help_text='Distrito',
        editable=False
    )
    delta_proceso = models.SmallIntegerField(
        help_text="Control de proceso",
        editable=False, null=True
    )

    usuario = models.ForeignKey(
        User, related_name='dpi_user',
        editable=False, on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['-fecha_tramite']
        indexes = [
            models.Index(fields=['folio', ], name='folio_idx')
        ]
        unique_together = ('tipo', 'folio')
        verbose_name = 'Expediente DPI'
        verbose_name_plural = 'Expedientes de DPI'

    def __str__(self):
        return f'{self.tipo}_{self.folio}'

    def save(self, *args, **kwargs):  # pylint: disable=W0221
        self.nombre = self.nombre.upper()
        self.entidad = self.folio[2:4]
        self.distrito = self.folio[4:6]
        self.delta_proceso = delta(self.tratamiento, self.resolucion)
        super(ExpedienteDPI, self).save(*args, **kwargs)

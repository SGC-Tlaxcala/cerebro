# coding: utf-8
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo = models.CharField(choices=TIPOS, max_length=3)
    folio = models.CharField(max_length=13)
    nombre = models.CharField(max_length=100)

    # Etapa de VRD
    fecha_tramite = models.DateField(null=True, blank=True)

    # Notificación/Aclaración de TRAMITE
    fecha_notificacion_aclaracion = models.DateField(
        'TRÁMITE: Notificación',
        help_text='Fecha de notificación de aclaración al ciudadano AC',
        null=True, blank=True
    )
    fecha_entrevista = models.DateField(
        help_text='TRÁMITE: Fecha de la entrevista o Acta Administrativa',
        null=True, blank=True
    )
    fecha_envio_expediente = models.DateField(
        help_text='TRÁMITE: Fecha de envío de expediente a la JL',
        null=True, blank=True
    )

    # Notificación/Aclaración de REGISTRO
    fecha_notificacion_registro = models.DateField(
        'REGISTRO: Notificación',
        help_text='Fecha de notificación de aclaración al ciudadano AC',
        null=True, blank=True
    )
    fecha_entrevista_registro = models.DateField(
        'REGISTRO: Entrevista/Acta',
        help_text='Fecha de la entrevista o Acta Administrativa',
        null=True, blank=True
    )
    fecha_envio_expediente_registro = models.DateField(
        'REGISTRO: Envio a JL',
        help_text='REGISTRO: Fecha de envío de expediente a la JL',
        null=True, blank=True
    )

    # Etapa VRL-VRD - Cédula de Verificación
    fecha_solicitud_cedula = models.DateField(
        help_text='Fecha de solicitud de cédula',
        null=True, blank=True
    )
    fecha_ejecucion_cedula = models.DateField(
        help_text='Fecha de ejecución de la cédula',
        null=True, blank=True
    )

    fecha_validacion_expediente = models.DateField(
        help_text='Fecha de validación de expediente',
        null=True, blank=True
    )

    # Notificación de estatus de trámite
    estado = models.PositiveSmallIntegerField(
        help_text='Estado del trámite',
        choices=ESTADO,
        default=NO_INDICA
    )
    fecha_notificacion_rechazo = models.DateField(
        help_text='Fecha de notificación de trámite rechazado RE',
        null=True, blank=True
    )
    fecha_notificacion_exclusion = models.DateField(
        help_text='Fecha de notificación de exclusión de registro',
        null=True, blank=True
    )

    # Cálculo de intervalos de tiempo
    entidad = models.PositiveSmallIntegerField(help_text='Entidad', editable=False)
    distrito = models.PositiveSmallIntegerField(help_text='Distrito', editable=False)
    delta_notificar = models.SmallIntegerField(
        help_text="Delta entre tramite y notificación",
        editable=False, null=True
    )
    delta_aclarar = models.SmallIntegerField(
        help_text="Delta entre notificación y entrevista",
        editable=False, null=True
    )
    delta_entrevista = models.SmallIntegerField(
        help_text="Delta entre notificación y entrevista",
        editable=False, null=True
    )
    delta_enviar = models.SmallIntegerField(
        help_text="Delta entre entrevista y envío a JL",
        editable=False, null=True
    )
    delta_distrito = models.SmallIntegerField(
        help_text="Delta entre tramite y envío a JL",
        editable=False, null=True
    )
    delta_verificar = models.SmallIntegerField(
        help_text="Delta entre solicitud de verificación y ejecución de la cédula",
        editable=False, null=True,
    )

    completo = models.PositiveSmallIntegerField(editable=False, null=False, default=0)
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

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.entidad = self.folio[2:4]
        self.distrito = self.folio[4:6]
        self.delta_notificar = delta(self.fecha_tramite, self.fecha_notificacion_aclaracion)
        self.delta_aclarar = delta(self.fecha_notificacion_aclaracion, self.fecha_entrevista)
        self.delta_entrevista = delta(self.fecha_notificacion_aclaracion, self.fecha_entrevista)
        self.delta_enviar = delta(self.fecha_entrevista, self.fecha_envio_expediente)
        self.delta_distrito = delta(self.fecha_tramite, self.fecha_envio_expediente)
        self.delta_verificar = delta(self.fecha_solicitud_cedula, self.fecha_ejecucion_cedula)
        if (self.fecha_tramite is not None and
                self.fecha_entrevista is not None and
                self.fecha_envio_expediente is not None and
                self.fecha_notificacion_aclaracion is not None):
            self.completo = 1
        else:
            self.completo = 0
        super(ExpedienteDPI, self).save(*args, **kwargs)

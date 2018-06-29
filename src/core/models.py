# coding: utf-8
#         app: cerebro
#      module: mx.ine.tlax.sgc.core.models
#        date: lunes, 28 de mayo de 2018 - 13:16
# description: Modelos de comportamiento comunes
# pylint: disable=W0613,R0201,R0903


from django.db import models
from django.conf import settings

B = 1
B1 = 2
B2 = 3
B3 = 4
B4 = 5
B5 = 6
B6 = 7
B7 = 8
B8 = 9
B9 = 10

ESTACIONES = (
    (B, 'Básico'),
    (B1, 'Básico + 1'),
    (B2, 'Básico + 2'),
    (B3, 'Básico + 3'),
    (B4, 'Básico + 4'),
    (B5, 'Básico + 5')
)

FIJO = 1
FIJO_ADICIONAL = 2
SEMIFIJO = 3
MOVIL = 4
URBANO = 5

TIPO_MAC = (
    (FIJO, 'Fijo Distrital'),
    (FIJO_ADICIONAL, 'Fijo Adicional'),
    (SEMIFIJO, 'Semifijo'),
    (MOVIL, 'Móvil'),
    (URBANO, 'Urbano Itinerante')
)


class TimeStampedModel(models.Model):
    """
    Una clase abstracta que sirve de base para modelos.
    Actualiza automáticamente los campos ``creado`` y ``modificado``.
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Modulo(TimeStampedModel):
    """Modelo para registro de macs."""
    distrito = models.PositiveSmallIntegerField()
    modulo = models.CharField('Módulo', max_length=6, help_text='Clave completa del MAC a 6 dígitos')

    class Meta:
        """Metadatos del modelo Modulo"""
        unique_together = (('distrito', 'modulo'), )

    def __str__(self):
        return self.modulo

    @property
    def actual(self):
        """Regresa la revisión actual."""
        return self.historialmodulo.first()


class HistorialModulo(TimeStampedModel):
    """Historial de configuraciones de módulo."""
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name="historialmodulo")
    tipo = models.PositiveSmallIntegerField('Tipo de Módulo', choices=TIPO_MAC)
    estaciones = models.PositiveSmallIntegerField('Estaciones', choices=ESTACIONES)
    doble_turno = models.BooleanField('Doble Turno', default=False)
    fecha_inicio = models.DateField("Inicio de operaciones")
    fecha_termino = models.DateField("Fecha de término de operaciones")
    horario = models.TextField(help_text='Escribe el horario del módulo')
    observaciones = models.TextField(help_text='Describe brevemente la razón del cambio')

    # Datos de identificación y seguimiento
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='historialMAC_user',
        on_delete=models.CASCADE,
        editable=False)

    class Meta:
        """Metadatos del modelo HistorialModulo."""
        ordering = ['-fecha_inicio']
        get_latest_by = 'fecha_inicio'

    def __str__(self):
        return "%s - %s: %s (%s)" % (
            self.modulo,
            self.modulo.historialmodulo.last().get_tipo_display(),
            self.modulo.historialmodulo.last().get_estaciones_display(),
            self.fecha_inicio
        )


class Remesa (models.Model):
    remesa = models.CharField(max_length=7)
    inicio = models.DateField()
    fin = models.DateField()

    def days(self):
        return self.fin - self.inicio

    def __str__(self):
        return f"Remesa {self.remesa}"

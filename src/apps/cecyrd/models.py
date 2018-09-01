# coding: utf-8
# app: cecyrd
# module: Evaluación del proveedor
# date: 01 Sep 2018
# author: Javier Sanchez Toledano <js.toledano@me.com>
"""Evalúa al proveedor y extrae otros datos importantes."""

from django.db import models


def get_tramo(reciente, anterior):
    try:
        return reciente - anterior
    except TypeError:
        return None


class Tramites(models.Model):
    # Identificación del trámite
    folio = models.CharField(primary_key=True, max_length=13)
    distrito = models.PositiveSmallIntegerField(editable=False)
    mac = models.CharField(max_length=6, editable=False)

    # Tramos de respuesta
    tramo_exitoso = models.DurationField(editable=False, blank=True, null=True)
    tramo_disponible = models.DurationField(editable=False, blank=True, null=True)
    tramo_entrega = models.DurationField(editable=False, blank=True, null=True)

    # Estatus del trámite
    estatus = models.TextField(blank=True, null=True)
    causa_rechazo = models.TextField(blank=True, null=True)
    movimiento_solicitado = models.TextField(blank=True, null=True)
    movimiento_definitivo = models.TextField(blank=True, null=True)

    # timestamps
    fecha_tramite = models.DateTimeField(blank=True, null=True)
    fecha_recibido_cecyrd = models.DateTimeField(blank=True, null=True)
    fecha_registrado_cecyrd = models.DateTimeField(blank=True, null=True)
    fecha_rechazado = models.DateTimeField(blank=True, null=True)
    fecha_cancelado_movimiento_posterior = models.DateTimeField(blank=True, null=True)
    fecha_alta_pe = models.DateTimeField(blank=True, null=True)
    fecha_afectacion_padron = models.DateTimeField(blank=True, null=True)
    fecha_actualizacion_pe = models.DateTimeField(blank=True, null=True)
    fecha_reincorporacion_pe = models.DateTimeField(blank=True, null=True)
    fecha_exitoso = models.DateTimeField(blank=True, null=True)
    fecha_lote_produccion = models.DateTimeField(blank=True, null=True)
    fecha_listo_reimpresion = models.DateTimeField(blank=True, null=True)
    fecha_cpv_creada = models.DateTimeField(blank=True, null=True)
    fecha_cpv_registrada_mac = models.DateTimeField(blank=True, null=True)
    fecha_cpv_disponible = models.DateTimeField(blank=True, null=True)
    fecha_cpv_entregada = models.DateTimeField(blank=True, null=True)
    fecha_afectacion_ln = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'cecyrd_tramites'

    def __str__(self):
        return self.folio

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.distrito = int(self.folio[5])
        self.mac = self.folio[2:8]
        self.tramo_entrega = get_tramo(self.fecha_cpv_entregada, self.fecha_cpv_disponible)
        self.tramo_disponible = get_tramo(self.fecha_cpv_disponible, self.fecha_tramite)
        self.tramo_exitoso = get_tramo(self.fecha_exitoso, self.fecha_tramite)
        super(Tramites, self).save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
        )

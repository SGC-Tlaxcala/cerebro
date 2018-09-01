# coding: utf-8
# app: cecyrd
# module: Evaluación del proveedor
# date: 01 Sep 2018
# author: Javier Sanchez Toledano <js.toledano@me.com>
"""Evalúa al proveedor y extrae otros datos importantes."""

from django.db import models


class Tramites(models.Model):
    folio = models.CharField(primary_key=True, max_length=13)
    distrito = models.PositiveSmallIntegerField()
    mac = models.CharField(max_length=6)

    estatus = models.TextField(blank=True, null=True)
    causa_rechazo = models.TextField(blank=True, null=True)
    movimiento_solicitado = models.TextField(blank=True, null=True)
    movimiento_definitivo = models.TextField(blank=True, null=True)
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

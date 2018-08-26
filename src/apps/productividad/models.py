# coding: utf-8
# app: apps.productividad.models
# author: Javier Sanchez Toledano <js.toledano@me.com>
# date: 26/08/2018
"""Modelos para control de la productividad."""

from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStampedModel


class Reporte(TimeStampedModel):
    """Modelo para el reporte de cifras."""
    fecha_corte = models.DateField('Fecha de Corte')
    remesa = models.CharField('Remesa', max_length=8, unique=True)
    notas = models.TextField('Observaciones')
    archivo = models.FileField('Archivo de cifras', upload_to='productividad')
    usuario = models.ForeignKey(
        User,
        related_name='productividad_user',
        editable=False,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Remesa {self.remesa}'

    class Meta:
        verbose_name = "Reporte de Productividad"
        verbose_name_plural = "Reportes de Productividad"
        ordering = ["-fecha_corte"]
        get_latest_by = 'fecha_corte'


class Cifras(models.Model):
    """Modelo de productividad."""
    reporte_semanal = models.ForeignKey(Reporte, on_delete=models.CASCADE)
    distrito = models.CharField('Distrito', max_length=2)
    modulo = models.CharField('Módulo', max_length=6)
    tipo = models.CharField('Tipo de módulo', max_length=20)
    dias_trabajados = models.PositiveSmallIntegerField('Días trabajados')
    jornada_trabajada = models.FloatField('Jornada trabajada')
    configuracion = models.CharField('Configuración', max_length=10)
    tramites = models.SmallIntegerField('Trámites')
    credenciales_entregadas_actualizacion = models.SmallIntegerField(
        'Credenciales entregas',
        help_text='Credenciales entregadas producto de trámites de actualización'
    )
    credenciales_reimpresion = models.SmallIntegerField(
        'Credenciales reimpresión',
        help_text='Credenciales entregadas productos de solicitudes de reimpresión'
    )
    total_atenciones = models.SmallIntegerField('Total de atención')
    productividad_x_dia = models.SmallIntegerField('Productividad por día')
    productividad_x_dia_x_estacion = models.SmallIntegerField('Productividad por día por estación')
    credenciales_recibidas = models.SmallIntegerField('Credenciales recibidas')

    def __str__(self):
        return f'{self.modulo} - {self.reporte_semanal.remesa}'

    class Meta:
        verbose_name = 'Cifras por módulo'
        verbose_name_plural = 'Reportes de productividad'
        ordering = ['distrito', 'modulo']

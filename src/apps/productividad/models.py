# coding: utf-8
# app: apps.productividad.models
# author: Javier Sanchez Toledano <js.toledano@me.com>
# date: 26/08/2018
"""Modelos para control de la productividad."""

from simple_history.models import HistoricalRecords
from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStampedModel


JD01 = 1
JD02 = 2
JD03 = 3
DISTRITOS = (
    (JD01, 'Distrito 01'),
    (JD02, 'Distrito 02'),
    (JD03, 'Distrito 03')
)


class PronosticoTramites(models.Model):
    """Modelo para el control de trámites"""
    year = models.PositiveSmallIntegerField('Año')
    distrito = models.PositiveSmallIntegerField(choices=DISTRITOS)
    tramites = models.IntegerField()
    historial = HistoricalRecords()

    class Meta:
        ordering = ('year', 'distrito')
        unique_together = (('year', 'distrito'), )
        verbose_name = 'Pronóstico'
        verbose_name_plural = 'Pronósticos de trámites'

    def __str__(self):
        return f'{self.get_distrito_display()} - {self.year}: {self.tramites}'


class Reporte(TimeStampedModel):
    """Modelo para el reporte de cifras."""
    fecha_corte = models.DateField('Fecha de Corte')
    remesa = models.CharField('Remesa', max_length=8, unique=True)
    notas = models.TextField('Observaciones')
    archivo = models.FileField('Archivo de cifras', upload_to='productividad', max_length=500)
    usuario = models.ForeignKey(
        User,
        related_name='cifras_user',
        editable=False,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Remesa {self.remesa}'

    class Meta:
        verbose_name = "Reporte de Productividad"
        verbose_name_plural = "Reportes de Productividad"
        get_latest_by = 'fecha_corte'


class Numbers(models.Model):
    """Modelo de productividad."""
    reporte_semanal = models.ForeignKey(
        Reporte,
        related_name='reporte_cifras',
        on_delete=models.CASCADE
    )
    distrito = models.CharField('Distrito', max_length=2)
    mac = models.CharField('Módulo', max_length=6)
    type = models.CharField('Tipo de módulo', max_length=20)
    days_worked = models.FloatField('Días trabajados')
    hours_worked = models.FloatField('Jornada trabajada')
    setup = models.CharField('Configuración', max_length=10)
    tramites_aplicados = models.SmallIntegerField('Trámites')
    cards_by_update = models.SmallIntegerField(
        'Credenciales entregadas',
        help_text='Credenciales entregadas producto de trámites de actualización'
    )
    total_atenciones = models.SmallIntegerField('Total de atención')
    numbers_by_day = models.SmallIntegerField('Productividad por día')
    numbers_by_machine_by_day = models.SmallIntegerField('Productividad por día por estación')
    credenciales_recibidas = models.SmallIntegerField('Credenciales recibidas')

    def __str__(self):
        return f'{self.mac} - {self.reporte_semanal.remesa}'

    class Meta:
        verbose_name = 'Cifras por módulo'
        verbose_name_plural = 'Reportes de productividad'
        ordering = ['distrito', 'mac']

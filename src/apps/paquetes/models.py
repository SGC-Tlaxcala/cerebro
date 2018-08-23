# coding: utf-8
# app: paquetes
# module: models
# date: 23 Aug 2018
# author: Javier Sanchez Toledano <js.toledano@me.com>
# description: Modelos para la app de distribución del paquetes.

import timedelta
from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStampedModel
from core.models import Remesa


class Parcel(TimeStampedModel):
    ACT = 1
    APEL = 2
    TIPO_CINTA = (
            (ACT, 'Actualizaciones'),
            (APEL, 'Recurso de Apelación'),
        )
    ORD = 1
    BIS = 2
    REI = 3
    RA = 4
    EXT = 5
    TIPO_LOTE = (
            (ORD, 'ORD'),
            (BIS, 'BIS'),
            (REI, 'REI'),
            (RA, 'RA'),
            (EXT, 'EXT'),
        )
    JD01 = 1
    JD02 = 2
    JD03 = 3
    DISTRITO = (
            (JD01, 'Apizaco - Distrito 01'),
            (JD02, 'Tlaxcala - Distrito 02'),
            (JD03, 'Zacatelco - Distrito 03'),
        )
    fecha_corte = models.DateField('Fecha de Corte', editable=False, null=True)
    distrito = models.CharField('Distrito', max_length=1, choices=DISTRITO)
    lote = models.CharField(max_length=11)
    tipo_lote = models.CharField('Tipo de Lote', max_length=3, choices=TIPO_LOTE)
    num_prod = models.CharField ('Número de Producción', max_length=7)
    tipo_cinta = models.CharField ('Tipo de Cinta', max_length=1, choices=TIPO_CINTA)
    modulos = models.PositiveSmallIntegerField('Número de Módulos')
    credenciales = models.IntegerField('Número de FCPVF en el envío')
    cajas = models.PositiveSmallIntegerField('Número de cajas')
    envio_cnd = models.DateTimeField('Fecha de envío CND')
    recibido_vrd=models.DateTimeField('Fecha de recibido en Vocalía Distrital')
    transito = timedelta.fields.TimedeltaField(editable=False)
    tran_sec = models.FloatField(editable=False)
    autor = models.ForeignKey(User, related_name='prod_parcel', editable=False, on_delete=models.CASCADE)

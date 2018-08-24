# coding: utf-8
# app: paquetes
# module: models
# date: 23 Aug 2018
# author: Javier Sanchez Toledano <js.toledano@me.com>
# description: Modelos para la app de distribución del paquetes.

from django.db import models
from django.contrib.auth.models import User
from core.models import Remesa, TimeStampedModel


class Envio(TimeStampedModel):
    ACTUALIZACION = 1
    APELACION = 2
    TIPO_CINTA = (
        (ACTUALIZACION, 'Actualizaciones'),
        (APELACION, 'Recurso de Apelación'),
    )

    ORD = 'ORD'
    BIS = 'BIS'
    REI = 'REI'
    RA = 'RA'
    EXT = 'EXT'
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
    num_prod = models.CharField('Número de Producción', max_length=7)
    tipo_cinta = models.CharField('Tipo de Cinta', max_length=1, choices=TIPO_CINTA)
    modulos = models.PositiveSmallIntegerField('Número de Módulos')
    credenciales = models.IntegerField('Número de FCPVF en el envio')
    cajas = models.PositiveSmallIntegerField('Número de cajas')
    envio_cnd = models.DateTimeField('Fecha de envio CND')
    recibido_vrd = models.DateTimeField('Fecha de recibido en Vocalía Distrital')
    transito = models.DurationField(editable=False)
    tran_sec = models.FloatField(editable=False)
    autor = models.ForeignKey(User, related_name='prod_parcel', editable=False, on_delete=models.CASCADE)

    def __str__(self):
        return f'Distrito 0{self.distrito} Lote: {self.lote}_{self.tipo_lote}'

    def save(self, *args, **kwargs):
        try:
            for rem in Remesa.objects.all():
                if rem.inicio <= self.recibido_vrd.date() <= rem.fin:
                    self.fecha_corte = rem.fin
        except Remesa.DoesNotExist:
            self.fecha_corte = None
        self.transito = self.recibido_vrd - self.envio_cnd
        self.tran_sec = self.transito.total_seconds()
        super(Envio, self).save(*args, **kwargs)

    def remesa(self):
        try:
            for rem in Remesa.objects.all():
                if rem.inicio <= self.fecha_corte <= rem.fin:
                    return rem.remesa
        except Remesa.DoesNotExist:
            return None

    remesa.short_description = "Remesa"

    @property
    def _get_transito(self):
        tran = self.recibido_vrd - self.envio_cnd
        return tran

    class Meta:
        verbose_name = "Envío"
        verbose_name_plural = "Envíos"
        unique_together = ('lote', 'distrito', 'recibido_vrd',)


class EnvioModulo (models.Model):
    MODULO = (
        ('151', '290151'),
        ('152', '290152'),
        ('153', '290153'),
        ('154', '290154'),
        ('251', '290251'),
        ('252', '290252'),
        ('253', '290253'),
        ('254', '290254'),
        ('351', '290351'),
        ('352', '290352'),
        ('353', '290353'),
    )
    lote = models.ForeignKey(Envio, on_delete=models.CASCADE)
    mac = models.CharField(max_length=3, choices=MODULO)
    paquetes = models.PositiveSmallIntegerField()
    formatos = models.IntegerField()
    recibido_mac = models.DateTimeField()
    disponible_mac = models.DateTimeField()
    transito = models.DurationField(editable=False)
    tran_sec = models.FloatField(editable=False)

    def __str__(self):
        return '290%s - %s' % (self.mac, self.lote)

    @property
    def _get_remesa(self):
            try:
                for rem in Remesa.objects.all():
                    if rem.inicio <= self.lote.fecha_corte <= rem.fin:
                        return rem
            except Remesa.DoesNotExist:
                return None

    def save(self, *args, **kwargs):
        self.transito = self.disponible_mac - self.lote.recibido_vrd
        self.tran_sec = self.transito.total_seconds()
        super(EnvioModulo, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Paquete"
        verbose_name_plural = "Paquetes a MAC"
        unique_together = ('lote', 'mac')

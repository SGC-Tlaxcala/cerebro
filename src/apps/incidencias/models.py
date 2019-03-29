# coding: utf-8
#         app: incidencias
#      module: models
#        date: miércoles, 13 de febrero de 2018 - 10:15
# description: Modelos para el control de incidencias

from django.db import models
from core.models import TimeStampedModel, Remesa


MODULOS = (
    ('290151', '290151'),
    ('290152', '290152'),
    ('290153', '290153'),
    ('290251', '290251'),
    ('290252', '290252'),
    ('290253', '290253'),
    ('290254', '290254'),
    ('290351', '290351'),
    ('290352', '290352'),
    ('290353', '290353'),
    ('999999', 'Todos los MAC')
)


CONFIGURACION = (
    (1, 'Básico'),
    (2, 'Básico + 1'),
    (3, 'Básico + 2'),
    (4, 'Básico + 3'),
    (5, 'Básico + 4'),
    (6, 'Básico + 5'),
    (7, 'Básico + 6')
)

FIJO_DISTRITAL = 1
FIJO_ADICIONAL = 2
SEMIFIJO = 3
MOVIL = 4

TIPO_MAC = (
    (FIJO_DISTRITAL, 'Fijo Distrital'),
    (FIJO_ADICIONAL, 'Fijo Adicional'),
    (SEMIFIJO, 'Semifijo'),
    (MOVIL, 'Móvil')
)


def remesa(fecha):
    for r in Remesa.objects.all():
        if r.inicio <= fecha.date() <= r.fin:
            return r.remesa


class Modulo(models.Model):
    distrito = models.PositiveSmallIntegerField('Distrito', editable=False)
    mac = models.CharField('Módulo', max_length=6)
    doble_turno = models.BooleanField()
    sabados = models.BooleanField()
    configuracion = models.PositiveSmallIntegerField('Configuración', choices=CONFIGURACION)
    dias = models.PositiveIntegerField()
    tipo_mac = models.PositiveSmallIntegerField(choices=TIPO_MAC)

    def __str__(self):
        return self.mac

    def save(self, *args, **kwargs):
        self.distrito = self.mac[3]
        super(Modulo, self).save(*args, **kwargs)


class Tipo(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.nombre}'


class Incidencia(TimeStampedModel):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField()
    fecha_final = models.DateTimeField()
    all_day = models.BooleanField("Todo el día")
    remesa = models.CharField('Remesa', max_length=7, editable=False, null=True)
    inhabilitado = models.BooleanField()
    caso_cau = models.CharField(max_length=15)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    descripcion = models.TextField()
    solucion = models.TextField()
    duracion = models.DurationField(editable=False, null=True)

    class Meta:
        verbose_name = 'Incidencia'
        verbose_name_plural = 'Incidencias'

    def __str__(self):
        return f'{self.modulo} - {self.caso_cau} - {self.remesa}'

    def save(self, *args, **kwargs):
        self.remesa = remesa(self.fecha_inicio)
        self.duracion = self.fecha_final - self.fecha_inicio
        super(Incidencia, self).save(*args, **kwargs)

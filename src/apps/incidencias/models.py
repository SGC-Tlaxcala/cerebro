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
    ('290353', '290353')
)


def remesa(fecha):
    for r in Remesa.objects.all():
        if r.inicio <= fecha.date() <= r.fin:
            return r.remesa


class Tipo(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.nombre}'


class Incidencia(TimeStampedModel):
    distrito = models.PositiveSmallIntegerField('Distrito', editable=False)
    modulo = models.CharField(max_length=6, choices=MODULOS)
    fecha_inicio = models.DateTimeField()
    fecha_final = models.DateTimeField()
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
        self.distrito = self.modulo[3]
        self.duracion = self.fecha_final - self.fecha_inicio
        super(Incidencia, self).save(*args, **kwargs)

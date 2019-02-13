# coding: utf-8
#         app: incidencias
#      module: models
#        date: miércoles, 13 de febrero de 2018 - 10:15
# description: Modelos para el control de incidencias
# pylint: disable=W0613,R0201,R0903


from django.db import models
from core.models import TimeStampedModel, Remesa


def remesa(fecha):
    for r in Remesa.objects.all():
        if r.inicio <= fecha <= r.fin:
            return r.remesa


class Tipo(models.Model):
    nombre = models.CharField(max_length=255)


class Incidencia(TimeStampedModel):
    distrito = models.PositiveSmallIntegerField()
    modulo = models.CharField(max_length=6)
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    remesa = models.CharField('Remesa', max_length=7, editable=False, null=True)
    inhabilitado = models.BooleanField()
    caso_cau = models.CharField(max_length=15)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    descripcion = models.TextField()
    solucion = models.TextField()

    class Meta:
        verbose_name = 'Incidencia'
        verbose_name_plural = 'Incidencias'

    def str(self):
        return f'{self.modulo} - {self.caso_cau}'

    def save(self, *args, **kwargs):
        self.remesa = remesa(self.fecha_inicio)
        self.distrito = self.modulo[3]
        super(Incidencia, self).save(*args, **kwargs)

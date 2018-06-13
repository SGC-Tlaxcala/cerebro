# coding: utf-8
#         app: mesa de atencion
#      module: models
#        date: miércoles, 13 de junio de 2018 - 14:30
# description: Modelos para la bitácora de rechazados en MAC
# pylint: disable=W0613,R0201,R0903


import uuid
from django.db import models
from core.models import TimeStampedModel, Remesa

HOMBRE = 'H'
MUJER = 'M'
SEXO = (
    HOMBRE, 'Hombre',
    MUJER, 'Mujer'
)

ACTA = 1
IDENTIFICACION = 2
COMPROBANTE = 3
INFORMACION = 4
ENTREGA = 5
FICHA = 6
EDAD = 7
HUELLA = 8
OTRO = 9
CAUSAS = (
    (ACTA, 'Falta el acta de nacimiento'),
    (IDENTIFICACION, 'Falta identificación'),
    (COMPROBANTE, 'Falta comprobante de domicilio'),
    (INFORMACION, 'Solo necesita información'),
    (ENTREGA, 'Va a recoger su CPV'),
    (FICHA, 'No hay mas fichas'),
    (EDAD, 'Menor de 18 años'),
    (HUELLA, 'No pasó la huella'),
    (OTRO, 'Otra causa')
)

BARRA = 1
MESA = 2
LUGAR = (
    (BARRA, 'Área de Trámite/Entrega'),
    (MESA, 'Mesa de atención')
)


def remesa(fecha):
    for r in Remesa.objects.all():
        if r.inicio <= fecha <= r.fin:
            return r.remesa


class Registro(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateField('Fecha')
    remesa = models.CharField('Remesa', max_length=7, editable=False, null=True)
    distrito = models.PositiveSmallIntegerField('Distrito')
    modulo = models.CharField('Módulo', max_length=3)
    lugar = models.PositiveSmallIntegerField('Lugar de atención')
    sexo = models.PositiveSmallIntegerField('Sexo', choices=SEXO)
    causa = models.PositiveSmallIntegerField('Causa', choices=CAUSAS)
    observaciones = models.TextField('Observaciones')

    class Meta:
        verbose_name = 'Registro de Atención'
        verbose_name_plural = 'Registros de Atención'

    def save(self, *args, **kwargs):
        self.remesa = remesa(self.fecha)
        super(Registro, self).save(*args, **kwargs)

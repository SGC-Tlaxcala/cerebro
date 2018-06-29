# coding: utf-8
#         app: mesa de atencion
#      module: models
#        date: miércoles, 13 de junio de 2018 - 14:30
# description: Modelos para la bitácora de rechazados en MAC
# pylint: disable=W0613,R0201,R0903

from django.db import models
from core.models import TimeStampedModel, Remesa

HOMBRE = 'H'
MUJER = 'M'
SEXO = (
           (HOMBRE, 'Hombre'),
           (MUJER, 'Mujer')
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
    (ACTA, '1. Falta el acta de nacimiento'),
    (IDENTIFICACION, '2. Falta identificación'),
    (COMPROBANTE, '3. Falta comprobante de domicilio'),
    (INFORMACION, '4. Solo necesita información'),
    (ENTREGA, '5. Va a recoger su CPV'),
    (FICHA, '6. No hay mas fichas'),
    (EDAD, '7. Menor de 18 años'),
    (HUELLA, '8. No pasó la huella'),
    (OTRO, '9. Otra causa')
)

BARRA = 1
MESA = 2
LUGAR = (
    (BARRA, 'Barra: Área de Trámite/Entrega'),
    (MESA, 'Mesa: Mesa de atención')
)


def remesa(fecha):
    for r in Remesa.objects.all():
        if r.inicio <= fecha <= r.fin:
            return r.remesa


class Registro(TimeStampedModel):
    SEXO = (
        (HOMBRE, 'Hombre'),
        (MUJER, 'Mujer')
    )

    CAUSAS = (
        (ACTA, '1. Falta el acta de nacimiento'),
        (IDENTIFICACION, '2. Falta identificación'),
        (COMPROBANTE, '3. Falta comprobante de domicilio'),
        (INFORMACION, '4. Solo necesita información'),
        (ENTREGA, '5. Va a recoger su CPV'),
        (FICHA, '6. No hay mas fichas'),
        (EDAD, '7. Menor de 18 años'),
        (HUELLA, '8. No pasó la huella'),
        (OTRO, '9. Otra causa')
    )

    LUGAR = (
        (BARRA, 'Barra: Área de Trámite/Entrega'),
        (MESA, 'Mesa: Mesa de atención')
    )

    fecha = models.DateField('Fecha')
    remesa = models.CharField('Remesa', max_length=7, editable=False, null=True)
    distrito = models.PositiveSmallIntegerField('Distrito', editable=False)
    modulo = models.CharField('Módulo', max_length=3)
    lugar = models.PositiveSmallIntegerField('Lugar de atención', choices=LUGAR)
    sexo = models.CharField('Sexo', choices=SEXO, max_length=1)
    causa = models.PositiveSmallIntegerField('Causa', choices=CAUSAS)
    observaciones = models.TextField('Observaciones', blank=True, null=True)

    class Meta:
        verbose_name = 'Registro de Atención'
        verbose_name_plural = 'Registros de Atención'

    def __str__(self):
        return f'{self.modulo} - Remesa: {self.remesa}'

    def save(self, *args, **kwargs):
        self.remesa = remesa(self.fecha)
        self.distrito = self.modulo[0]
        super(Registro, self).save(*args, **kwargs)

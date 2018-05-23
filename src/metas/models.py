# coding: utf-8
#         app: metas
#      módulo: models
# descripción: Modelos para las metas SPEN
#       autor: toledano
#       fecha: mar, 22 de mayo de 2018 07:29 PM

import uuid
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

from profiles.models import PUESTOS


def archivo_soporte(instancia, archivo):
    """Función para subir archivo"""
    import os.path
    ext = archivo.split('.')[-1]
    orig = 'metas'
    modelo = instancia.modelo()
    archivo = f'{modelo}_soporte.{ext}'
    meta = f"{instancia.puesto.lower()}-{instancia.clave}"
    ruta = os.path.join(orig, instancia.puesto.lower(), meta, archivo)
    return ruta


# Meta información sobre las Metas
class MetasSPE(models.Model):
    """Descripción de las metas del SPEN"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    puesto = models.CharField("Cargo", max_length=6, choices=PUESTOS)
    clave = models.CharField("Clave de la Meta", max_length=2)
    nom_corto = models.CharField('Identificación', max_length=25)
    year = models.PositiveIntegerField("Año")
    eval = models.BooleanField('Evaluación', default=True)

    # Seguimiento y Medición
    ciclos = models.PositiveSmallIntegerField('Repeticiones')

    # Descripción de la Meta
    description = models.TextField('Descripción de la Meta')
    description = models.TextField('Descripción de la Meta')
    soporte = models.FileField(
        'Soporte', upload_to = archivo_soporte, blank=True, null=True
    )

    # Datos de identificación y seguimiento
    usuario = models.ForeignKey(User, related_name='meta_user', editable=False, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField (auto_now = True)

    class Meta:
        verbose_name = "Meta"
        verbose_name_plural = "Control de Metas del SPE"
        app_label = 'metas'

    def __str__(self):
        return f'{self.puesto}-{self.clave}'
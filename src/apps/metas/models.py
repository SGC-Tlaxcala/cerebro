# coding: utf-8
#         app: metas
#      módulo: models
# descripción: Modelos para las metas SPEN
#       autor: toledano
#       fecha: mar, 22 de mayo de 2018 07:29 PM

import uuid
from unipath import Path
from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.template.defaultfilters import slugify


def archivo_soporte(instancia, archivo):
    """Función para subir archivo"""
    ext = archivo.split('.')[-1]
    orig = 'metas'
    modelo = f"{instancia.puesto}-{instancia.clave}"
    archivo = f'{modelo}_soporte.{ext}'
    meta = f"{instancia.puesto.lower()}-{instancia.clave}"
    ruta = Path(orig, instancia.puesto.lower(), meta, archivo)
    return ruta


def subir_archivo(instancia, archivo):
    ext = archivo.split('.')[-1]
    orig = 'metas'
    miembro = instancia.miembro.profile.position
    clave = "%02d" % int(instancia.meta.clave)
    sitio = slugify(instancia.miembro.profile.site)
    fecha = instancia.fecha.strftime('%y%m%d')
    meta = "%s-%s" % (miembro, clave)
    archivo = '%s_%s_%s.%s' % (meta, sitio, fecha, ext)
    ruta = Path(orig, miembro, meta, archivo)
    return ruta


class Site(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    site = models.CharField("Sitio", max_length=4)
    name = models.CharField("Nombre", max_length=50, default='')
    address = models.CharField("Dirección", max_length=100)

    def __str__(self):
        return f'{self.site}'


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clave = models.CharField("Clave del Puesto", max_length=7)
    description = models.CharField("Descripción", max_length=75)
    order = models.PositiveSmallIntegerField("Orden")

    def __str__(self):
        return f'{self.clave}'


class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Nombre", max_length=50)
    mail = models.CharField("Correo Electrónico", max_length=50)
    role = models.ForeignKey(Role, verbose_name='Puesto', related_name='member_role', on_delete=models.CASCADE)
    site = models.ForeignKey(Site, verbose_name='Sitio', related_name='member_site', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


# Meta información sobre las Metas
class Goal(models.Model):
    """Descripción de las metas del SPEN"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, verbose_name="Puesto", related_name='goal_role', on_delete=models.CASCADE)
    key = models.CharField("Clave de la Meta", max_length=2)
    name = models.CharField('Identificación', max_length=25)
    year = models.PositiveIntegerField("Año")

    # Seguimiento y Medición
    loops = models.PositiveSmallIntegerField('Repeticiones')

    # Descripción de la Meta
    description = models.TextField('Descripción de la Meta')
    support = models.FileField(
        'Soporte', upload_to=archivo_soporte, blank=True, null=True
    )

    # Evidencias
    fields = JSONField(blank=True, null=True)

    # Datos de identificación y seguimiento
    user = models.ForeignKey(User, related_name='goal_user', editable=False, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Meta"
        verbose_name_plural = "Control de Metas del SPE"
        app_label = 'metas'

    def __str__(self):
        return f'{self.role}-{self.key}'


class Proof(models.Model):
    """Identificación de la meta"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(
        Member, verbose_name='Miembro del SPE', related_name='proof_member', on_delete=models.CASCADE
    )
    goal = models.ForeignKey(Goal, verbose_name="Meta", related_name="proof_goal", on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Fecha")
    fields = JSONField(verbose_name="Campos", blank=True, null=True)
    user = models.ForeignKey(
        User, related_name='proof_user', editable=False, on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def pre_archivo(self):
        return f"{self.member.site}_{self.goal}_{self.date.strftime('%Y%m%d')}"

    def __str__(self):
        return "%s - %s - %s" % (self.goal, self.member.site, self.date)

    class Meta:
        app_label = 'metas'
        verbose_name_plural = "Evidencias"
        verbose_name = "Evidencia"

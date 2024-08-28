import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from tinymce.models import HTMLField


User = get_user_model()


class TrackingFields(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


PROCESO = (
    (1, 'Planeación'),
    (2, 'Apoyo Soporte'),
    (3, 'Clave'),
    (4, 'MSA'),
    (5, 'SGC'),
)

TIPO = (
    (1, 'Reactivo'),
    (2, 'Incremental'),
    (3, 'Innovación'),
    (4, 'Avance'),
    (5, 'Transformación'),
)

DETECCION = (
    (1, 'Auditoria Interna'),
    (2, 'Auditoria Externa'),
    (3, 'Revisión por los Vocales'),
    (4, 'Quejas'),
    (5, 'Otros'),
)

MEJORA = (
    (1, 'Procesos'),
    (2, 'Servicio'),
    (3, 'Sistema')
)

CERRADA = 99

A_ESTADO = (
    (1, u'Seguimiento'),
    (2, u'Revisión de Evidencia'),
    (3, u'En espera de una respuesta'),
    (4, u'En espera de una acción'),
    (5, u'En espera de un evento'),
    (CERRADA, u'Cerrada')
)

JPG = 'image/jpeg'
PDF = 'application/pdf'
PNG = 'image/png'


class Plan(models.Model):

    class Meta:
        verbose_name = _(u'Plan de Acción')
        verbose_name_plural = _(u'Planes de Acción')

    # #################################### #
    # I. Identificación del plan
    fecha_llenado = models.DateField(
        'Fecha de Llenado',
        default=datetime.date.today()
    )
    fecha_deteccion = models.DateField('Fecha de Detección')
    proceso = models.PositiveSmallIntegerField(choices=PROCESO)
    tipo = models.PositiveSmallIntegerField(choices=TIPO)
    deteccion = models.PositiveSmallIntegerField(choices=DETECCION)
    mejora = models.PositiveSmallIntegerField(choices=MEJORA)
    nombre = models.CharField(max_length=40)

    # #################################### #
    # II. Revisión
    redaccion = HTMLField(default='', blank=True, null=True)
    declaracion = HTMLField(default='', blank=True, null=True)
    evidencia = HTMLField(default='', blank=True, null=True)
    requisitos = HTMLField(default='', blank=True, null=True)
    relacionadas = HTMLField(default='', blank=True, null=True)

    # #################################### #
    # III. Responsabilidades
    informacion = models.CharField(max_length=30, blank=True, null=True)
    aplicacion = models.CharField(max_length=30, blank=True, null=True)
    responsable = models.CharField(max_length=30, blank=True, null=True)

    # #################################### #
    # IV. Reacción
    correccion = HTMLField(default="", blank=True, null=True)
    consecuencias = models.FileField(upload_to='pas', blank=True, null=True)
    reaccion_responsable = models.ForeignKey(
        User, blank=True, null=True)
    reaccion_evidencia = models.FileField(upload_to='pas', blank=True, null=True)

    # #################################### #
    # V. Determinación de las Causas
    pescadito = models.FileField(upload_to='pas', blank=True, null=True)
    cincopq = models.FileField('5 Por qués', upload_to='pas', blank=True, null=True)
    causa_raiz = HTMLField(default='', blank=True, null=True)

    # #################################### #
    # VI. Implementación de Acciones

    # #################################### #
    # VII. Revisión de la eficacia de las acciones

    # #################################### #
    # VIII. Cierre
    eliminacion = models.BooleanField(default=False)
    txt_eliminacion = HTMLField(blank=True, null=True)
    recurrencia = models.BooleanField(default=False)
    txt_recuerrencia = HTMLField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.nombre


class Accion(models.Model):
    class Meta:
        verbose_name = _(u'Acción Correctiva')
        verbose_name_plural = _('Acciones Correctivas')
    plan = models.ForeignKey(Plan)
    accion = HTMLField()
    recursos = HTMLField(blank=True, null=True)
    fecha = models.DateField()
    responsable = models.ForeignKey(Pipol)

    def _get_estado(self):
        "Regresa el estado de una acción correctiva, de acuerdo al último seguimiento capturado"
        if self.seguimiento_set.count() == 0:
            if self.fecha >= datetime.date.today():
                return 'Abierta en Tiempo'
            else:
                return 'Abierta Fuera de Tiempo'
        else:
            return self.seguimiento_set.latest().get_estado_display()
    estado = property(_get_estado)

    def __unicode__(self):
        return u'%s - %s: %s' % (self.id, self.plan, self.estado)


class Seguimiento(TrackingFields, models.Model):
    class Meta:
        verbose_name = _(u'Seguimiento de Acciones')
        verbose_name_plural = _('Seguimiento')
        get_latest_by = 'fecha'
        # get_latest_by = 'modified'
    accion = models.ForeignKey(Accion)
    descripcion = HTMLField()
    fecha = models.DateField()
    evidencia = models.FileField(upload_to='pas', blank=True, null=True)
    estado = models.PositiveSmallIntegerField(choices=A_ESTADO)
    responsable = models.ForeignKey(Pipol)

    def __unicode__(self):
        return u'%s - %s: %s' % (self.accion, self.fecha, self.get_estado_display())

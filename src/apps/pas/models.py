import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from tinymce.models import HTMLField


User = get_user_model()


class TrackingFields(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


CNC = 1
PCM = 2
DOCUMENTO = (
    (CNC, 'Cédula de No Conformidad'),
    (PCM, 'Plan de Cambios y Mejoras al SGC')
)

PROCESO = (
    (1, 'Estratégico'),
    (2, 'Sustantivos'),
    (3, 'Soporte'),
    (4, 'Medición, Análisis y Mejora'),
    (5, 'SGC'),
)

TIPO = (
    (1, 'Corrección'),
    (2, 'Acción Correctiva'),
    (3, 'Riesgo')
)

FUENTE = (
    (1, 'Auditoría Externa'),
    (2, 'Auditoría Interna'),
    (3, 'Queja del cliente'),
    (4, 'Revisión por la Dirección'),
    (5, 'Proceso'),
    (6, 'Documentación del SGC'),
    (7, 'Objetivos e Indicadores'),
    (8, 'Evaluación de riesgos'),
    (9, 'Otros')
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


class Plan(TrackingFields):

    class Meta:
        verbose_name = _(u'Plan de Acción')
        verbose_name_plural = _(u'Planes de Acción')

    # #################################### #
    # I. Campos de identificación comunes CNC y PCM
    nombre = models.CharField(max_length=255, help_text='Nombre del Plan de Acción')
    documento = models.IntegerField(choices=DOCUMENTO)
    folio = models.CharField(max_length=20)
    fecha_llenado = models.DateField(
        'Fecha de Llenado',
        default=datetime.date.today()
    )
    fecha_deteccion = models.DateField('Fecha de Detección', blank=True, null=True)

    # I.1 Identificación de la CNC
    tipo = models.IntegerField(choices=TIPO, help_text='Tipo de acción requerida')
    desc_cnc = HTMLField(default='', blank=True, null=True)
    fuente = models.IntegerField(choices=FUENTE)
    otra_fuente = models.TextField(blank=True, null=True)

    # I.2 Identificación del PCM
    fecha_termino = models.DateField('Fecha de Término', blank=True, null=True)
    proposito = models.TextField(blank=True, null=True, help_text='Propósito del cambio o mejora al SGC')
    requisito = models.TextField(
        blank=True, null=True,
        help_text='Requisito(s) de ISO 9001:2015 afectado(s) y/o beneficiados')
    proceso = models.PositiveSmallIntegerField(choices=PROCESO)
    desc_pcm = HTMLField(default='', blank=True, null=True, help_text='Descripción del cambio o mejora al SGC')
    consecuencias = HTMLField(
        default='', blank=True, null=True,
        help_text='Consecuencias potenciales de que el cambio o mejora no se realice')

    # #################################### #
    # II. Análisis de la CNC o PCM
    analisis = HTMLField(default='', blank=True, null=True, help_text='Análisis de la causa raíz')
    correccion = HTMLField(default='', blank=True, null=True, help_text='Corrección (si aplica)')
    evidencia_analisis = models.FileField(upload_to='pas', blank=True, null=True)

    # #################################### #
    # VIII. Cierre
    eliminacion = models.BooleanField(default=False)
    txt_eliminacion = HTMLField(blank=True, null=True)
    recurrencia = models.BooleanField(default=False)
    txt_recurrencia = HTMLField(blank=True, null=True)

    def __str__(self):
        return u'%s - %s' % (self.id, self.nombre)


class Accion(TrackingFields):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    accion = HTMLField()
    recursos = HTMLField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    responsable = models.ForeignKey(User, related_name='pas_responsable', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _(u'Actividad')
        verbose_name_plural = _('Actividades')

    @property
    def get_estado(self):
        """Regresa el estado de una acción correctiva, de acuerdo al último seguimiento capturado."""
        if self.seguimiento_set.count() == 0:
            if self.fecha_fin >= datetime.date.today():
                return 'Abierta en Tiempo'
            else:
                return 'Abierta Fuera de Tiempo'
        else:
            return self.seguimiento_set.latest().get_estado_display()

    def __str__(self):
        return f'{self.id} - {self.plan}: {self.get_estado}'


class Seguimiento(TrackingFields, models.Model):
    accion = models.ForeignKey(Accion, on_delete=models.CASCADE)
    descripcion = HTMLField()
    fecha = models.DateField()
    evidencia = models.FileField(upload_to='pas', blank=True, null=True)
    estado = models.PositiveSmallIntegerField(choices=A_ESTADO)
    responsable = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _(u'Seguimiento de Acciones')
        verbose_name_plural = _('Seguimiento')
        get_latest_by = 'fecha'
        # get_latest_by = 'modified'

    def __str__(self):
        return f'{self.accion} - {self.fecha}: {self.get_estado_display()}'

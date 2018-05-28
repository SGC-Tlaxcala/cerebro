# coding: utf-8
#         app: cmi.dpi
#      module: admin
#        date: lunes, 28 de mayo de 2018 - 14:54
# description: Área administrativa de la gestión de DPI y USI
# pylint: disable=W0613,R0201,R0903


from django.contrib import admin
from dpi.models import ExpedienteDPI


class ExpedienteDPIAdmin(admin.ModelAdmin):
    list_display = ('folio', 'fecha_tramite', 'fecha_envio_expediente', 'delta_distrito')
    list_filter = ('tipo', 'distrito', )
    fieldsets = (
        (None, {
            'fields': ('tipo', 'folio', 'nombre', 'tramite')
        }),
        ('Etapa de Aclaración', {
            'fields': ('fecha_notificacion_aclaracion', 'fecha_entrevista', 'fecha_envio_expediente')
        }),
        ('Etapa de Validación', {
            'fields': ('fecha_solicitud_cedula', 'fecha_ejecucion_cedula', 'fecha_validacion_expediente')
        }),
        ('Etapa de notificación de rechazo', {
            'fields': ('estado', 'fecha_notificacion_rechazo', 'fecha_notificacion_exclusion')
        })
    )

    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        obj.save()


admin.site.register(ExpedienteDPI, ExpedienteDPIAdmin)

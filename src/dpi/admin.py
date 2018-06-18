# coding: utf-8
#         app: cmi.dpi
#      module: admin
#        date: lunes, 28 de mayo de 2018 - 14:54
# description: Área administrativa de la gestión de DPI y USI
# pylint: disable=W0613,R0201,R0903


from django.contrib import admin
from dpi.models import ExpedienteDPI
from django import forms


class ExpedienteDPIForm(forms.ModelForm):

    class Meta:
        model = ExpedienteDPI
        fields = '__all__'

    def clean(self):
        fecha_tramite = self.cleaned_data.get('fecha_tramite')
        fecha_notificacion_aclaracion = self.cleaned_data.get('fecha_notificacion_aclaracion')
        fecha_entrevista = self.cleaned_data.get('fecha_entrevista')
        fecha_envio_expediente = self.cleaned_data.get('fecha_envio_expediente')
        if (fecha_tramite and fecha_notificacion_aclaracion) and fecha_tramite > fecha_notificacion_aclaracion:
            raise forms.ValidationError('La fecha de notificación debe ser posterior al trámite')
        if (fecha_tramite and fecha_entrevista) and fecha_tramite > fecha_entrevista:
            raise forms.ValidationError('La fecha de entrevista debe ser posterior al trámite')
        if (fecha_tramite and fecha_envio_expediente) and fecha_tramite > fecha_envio_expediente:
            raise forms.ValidationError('La fecha del oficio debe ser posterior al trámite')
        return self.cleaned_data


class ExpedienteDPIAdmin(admin.ModelAdmin):
    form = ExpedienteDPIForm
    list_display = ('folio', 'tipo', 'delta_distrito', 'completo')
    list_filter = ('completo', 'tipo', 'entidad', 'distrito')
    fieldsets = (
        (None, {
            'fields': (('tipo', 'folio'), ('nombre', 'fecha_tramite'))
        }),
        ('TRÁMITE: Etapa de Aclaración', {
            'fields': (('fecha_notificacion_aclaracion', 'fecha_entrevista', 'estado'), 'fecha_envio_expediente')
        }),
        ('REGISTRO: Etapa de Aclaración', {
            'classes': ('collapse',),
            'fields': (('fecha_notificacion_registro', 'fecha_entrevista_registro'), 'fecha_envio_expediente_registro')
        }),
        ('Etapa de Validación', {
            'classes': ('collapse',),
            'fields': (('fecha_solicitud_cedula', 'fecha_ejecucion_cedula', 'fecha_validacion_expediente'), )
        }),
        ('Etapa de notificación de rechazo', {
            'classes': ('collapse',),
            'fields': (('fecha_notificacion_rechazo', 'fecha_notificacion_exclusion'), )
        })
    )

    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        obj.save()


admin.site.register(ExpedienteDPI, ExpedienteDPIAdmin)

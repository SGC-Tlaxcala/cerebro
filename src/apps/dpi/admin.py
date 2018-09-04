# coding: utf-8
#         app: cmi.dpi
#      module: admin
#        date: lunes, 28 de mayo de 2018 - 14:54
# description: Área administrativa de la gestión de DPI y USI
# pylint: disable=W0613,R0201,R0903

from django.contrib import admin
from django import forms
from apps.dpi.models import ExpedienteDPI


class ExpedienteDPIForm(forms.ModelForm):

    class Meta:
        model = ExpedienteDPI
        fields = '__all__'

    def clean(self):
        fecha_tramite = self.cleaned_data.get('fecha_tramite')
        tratamiento = self.cleaned_data.get('tratamiento')
        captura = self.cleaned_data.get('captura')
        atencion = self.cleaned_data.get('atencion')
        resolucion = self.cleaned_data.get('resolucion')
        if fecha_tramite > tratamiento:
            raise forms.ValidationError('La fecha de "enviado a tratamiento" debe ser posterior al trámite')
        if tratamiento > captura:
            raise forms.ValidationError(
                'La fecha de "proceso de captura" debe ser posterior a la fecha de envio a tratamiento')
        if captura > atencion:
            raise forms.ValidationError(
                'La fecha de "pendiente de atención en JL" debe ser posterior a la fecha de captura '
            )
        if resolucion > atencion:
            raise forms.ValidationError(
                'La fecha de "pendiente de resolución" debe ser posterior a la fecha de "pendiente de atención en JL"'
            )

        return self.cleaned_data


class ExpedienteDPIAdmin(admin.ModelAdmin):
    form = ExpedienteDPIForm
    list_display = ('folio', 'tipo')
    list_filter = ('tipo', 'entidad', 'distrito')
    fieldsets = (
        (None, {
            'fields': (('tipo', 'folio'), ('nombre', 'fecha_tramite'))
        }),
        ('Datos del Procesador de Trámites en Análisis Registral', {
            'fields': (('tratamiento', 'captura'), ('atencion', 'resolucion'))
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        obj.save()


admin.site.register(ExpedienteDPI, ExpedienteDPIAdmin)

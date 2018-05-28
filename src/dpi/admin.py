# coding: utf-8
#         app: cmi.dpi
#      module: admin
#        date: lunes, 28 de mayo de 2018 - 14:54
# description: Área administrativa de la gestión de DPI y USI
# pylint: disable=W0613,R0201,R0903


from django.contrib import admin
from dpi.models import ExpedienteDPI


class ExpedienteDPIAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'folio', 'fecha_tramite', 'fecha_envio_expediente')
    list_filter = ('tipo')

    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        obj.save()


admin.site.register(ExpedienteDPI, ExpedienteDPIAdmin)

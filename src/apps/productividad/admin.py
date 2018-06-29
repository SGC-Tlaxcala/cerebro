# coding: utf-8
#      nombre: Área administrativa Productividad
#         app: Productividad
#   namespace: us.nspaces.sherpa.productividad
#       fecha: 09/10/2017 - 03:16 PM
# descripción: Configuración del área administrativa
# pylint: disable=W0613,R0201,C0111


from django.contrib import admin
from apps.productividad.models import ReporteSemanal, Cifras


# Modelos de Administración
class CifrasInline(admin.TabularInline):
    """Gestión de cifras inline."""

    model = Cifras
    extra = 1

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


class ReporteSemanalAdmin(admin.ModelAdmin):
    """Gestión de reportes semanales."""

    list_display = ('remesa', 'fecha_corte')
    list_filter = ['remesa']
    date_hierarchy = 'fecha_corte'
    inlines = [CifrasInline]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class CifrasAdmin(admin.ModelAdmin):
    """Gestión de cifras semanales."""

    list_display = ('reporte_semanal', 'modulo', 'prod_dia_est', 'atenciones')
    list_filter = ['reporte_semanal', 'reporte_semanal__fecha_corte', 'modulo__distrito', 'modulo']
    date_hierarchy = 'reporte_semanal__fecha_corte'

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


admin.site.register(ReporteSemanal, ReporteSemanalAdmin)
admin.site.register(Cifras, CifrasAdmin)
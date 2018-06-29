# coding: utf-8
__author__ = 'Javier Sanchez Toledano'

from django.contrib import admin
from core.models import Modulo, HistorialModulo


class HistorialModuloInline(admin.TabularInline):
    """Lista de historial por módulo."""

    model = HistorialModulo
    exclude = ('user', )
    extra = 0


class ModulosAdmin(admin.ModelAdmin):
    """Gestión de módulos."""
    list_display = ('distrito', 'modulo','periodo', 'tipo', 'revisiones')
    list_display_links = ('modulo', )
    list_filter = ('distrito', 'modulo')
    exclude = ('author', )
    inlines = [HistorialModuloInline]
    ordering = ['distrito', 'modulo']

    def revision_actual(self, obj):
        if obj.historialmodulo.last():
            return obj.actual.fecha_inicio
        else:
            return '-'

    def tipo(self, mac):
        if mac.historialmodulo.last():
            return mac.historialmodulo.last().get_tipo_display()
        else:
            return '-'

    def revisiones(self, mac):
        return mac.historialmodulo.count()

    def periodo(self, mac):
        if mac.actual:
            return f'De {mac.actual.fecha_inicio.strftime("%d/%m/%y")} a {mac.actual.fecha_termino.strftime("%d/%m/%y")}'
        else:
            return '-'

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.user = request.user
            instance.save()
        formset.save_m2m()


admin.site.register(Modulo, ModulosAdmin)

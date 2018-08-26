# coding: utf-8
# app: paquetes
# module: admin
# date: 23 Aug 2018
# author: Javier Sanchez Toledano <js.toledano@me.com>
"""Admin area for parcels control"""

from django.contrib import admin
from apps.paquetes.models import Envio, EnvioModulo


class EnvioModuloInline(admin.TabularInline):
    """Formulario que se inserta en el administrador"""
    model = EnvioModulo
    extra = 2


class EnvioModuloAdmin(admin.ModelAdmin):
    """Clase principal para administrar paquetes"""
    list_display = ('lote', 'mac', 'recibido_mac', 'paquetes', 'formatos')
    list_filter = ['mac', 'lote__distrito']
    date_hierarchy = 'recibido_mac'
    list_per_page = 25
    search_fields = ['lote__lote', 'mac']
    actions_selection_counter = True


class EnvioAdmin(admin.ModelAdmin):
    """Clase principal para administrar envíos"""
    list_display = (
        'distrito',
        'lote',
        'recibido_vrd',
        'fecha_corte',
        'transito',
        'credenciales',
        'cajas'
    )
    list_filter = ['distrito', 'lote', ]
    date_hierarchy = 'fecha_corte'
    inlines = [EnvioModuloInline]

    def save_model(self, request, obj, form, change):
        obj.autor = request.user
        obj.save()


admin.site.register(Envio, EnvioAdmin)
admin.site.register(EnvioModulo, EnvioModuloAdmin)

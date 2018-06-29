# coding: utf-8
#         app: metas
#      módulo: admin
# descripción: Área administrativa para las metas SPEN
#       autor: toledano
#       fecha: mar, 22 de mayo de 2018 07:59 PM


from django.contrib import admin
from apps.metas.models import MetasSPE
from apps.metas.models import Evidencia


class MetasAdmin(admin.ModelAdmin):
    list_display = ('nom_corto', 'puesto', 'clave')
    list_filter = ('puesto',)

    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        obj.save()


class EvidenciaAdmin(admin.ModelAdmin):
    pass

    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        obj.save()


admin.site.register(MetasSPE, MetasAdmin)
admin.site.register(Evidencia, EvidenciaAdmin)

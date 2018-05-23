# coding: utf-8
#         app: metas
#      módulo: admin
# descripción: Área administrativa para las metas SPEN
#       autor: toledano
#       fecha: mar, 22 de mayo de 2018 07:59 PM


from django.contrib import admin
from metas.models import MetasSPE
from metas.models import JMM01


class MetasAdmin(admin.ModelAdmin):
    list_display = ('nom_corto', 'puesto', 'clave')
    list_filter = ('puesto',)

    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        obj.save()


class JMM01Admin(admin.ModelAdmin):
    pass

    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        obj.save()


admin.site.register(MetasSPE, MetasAdmin)
admin.site.register(JMM01, JMM01Admin)

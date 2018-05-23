# coding: utf-8
#         app: metas
#      módulo: admin
# descripción: Área administrativa para las metas SPEN
#       autor: toledano
#       fecha: mar, 22 de mayo de 2018 07:59 PM


from django.contrib import admin
from metas.models import MetasSPE


class MetasAdmin(admin.ModelAdmin):
    list_display = ('nom_corto', 'puesto', 'clave')
    list_filter = ('puesto',)


admin.site.register(MetasSPE, MetasAdmin)

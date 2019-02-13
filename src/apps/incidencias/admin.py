# coding: utf-8
#         app: mesa de atencion
#      module: admin
#        date: miércoles, 13 de junio de 2018 - 16:20
# description: Área administrativa de la app Mesas de Atención
# pylint: disable=W0613,R0201,R0903


from django.contrib import admin
from apps.incidencias.models import Tipo, Incidencia


class TipoAdmin(admin.ModelAdmin):
    class Meta:
        fields = '__all__'
        model = Tipo


class IncidenciaAdmin(admin.ModelAdmin):
    class Meta:
        fields = '__all__'
        model = Incidencia


admin.site.register(Incidencia, IncidenciaAdmin)
admin.site.register(Tipo, TipoAdmin)

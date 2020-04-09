# coding: utf-8
#         app: metas
#      módulo: admin
# descripción: Área administrativa para las metas SPEN
#       autor: toledano
#       fecha: mar, 22 de mayo de 2018 07:59 PM


from django.contrib import admin
from apps.metas.models import Goal, Proof


class GoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'key')
    list_filter = ('role',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class ProofAdmin(admin.ModelAdmin):
    pass

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


admin.site.register(Goal, GoalAdmin)
admin.site.register(Proof, ProofAdmin)

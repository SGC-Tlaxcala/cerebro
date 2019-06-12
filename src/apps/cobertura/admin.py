from django.contrib import admin
from apps.cobertura.models import Cobertura


class CoberturaAdmin(admin.ModelAdmin):
    list_display = ('mes', 'pe', 'ln', 'dif', 'cobertura')
    list_filter = ('fecha', )

    def cobertura(self, obj):
        return f'{"{:.2%}".format(obj.cob)}'

    def mes(self, obj):
        return f'{obj.fecha.strftime("%Y-%m")}'

    def pe(self, obj):
        return f'{format(obj.padron, ",d")}'

    def ln(self, obj):
        return f'{format(obj.lista, ",d")}'

    def dif(self, data):
        return f'{format(data.diferencia, ",d")}'

    class Meta:
        fields = '__all__'
        model = Cobertura


admin.site.register(Cobertura, CoberturaAdmin)

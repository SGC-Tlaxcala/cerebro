from django.contrib import admin
from apps.cobertura.models import Cobertura


class CoberturaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'padron', 'lista', 'diferencia', 'cob')
    list_filter = ('fecha', )

    class Meta:
        fields = '__all__'
        model = Cobertura


admin.site.register(Cobertura, CoberturaAdmin)

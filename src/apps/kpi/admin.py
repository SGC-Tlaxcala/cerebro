from django.contrib import admin
from .models import Campaign, TramiteMensual


# Agrega al modelo Campaign un inline con los tramites mensuales
class TramiteMensualInline(admin.TabularInline):
    model = TramiteMensual
    extra = 1
    fields = ('month', 'tramites')


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('type', 'year', 'goal', 'forecast', 'acumulado', 'avance_percent')
    search_fields = ('type', 'year')
    inlines = [TramiteMensualInline]
    list_filter = ('type', 'year')

    def avance_percent(self, obj):
        return f"{obj.avance:.2f}%"
    avance_percent.short_description = "Avance"

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('acumulado','avance_percent')
        return self.readonly_fields


admin.site.register(Campaign, CampaignAdmin)

from django.contrib import admin
from apps.aprobacion.models import Aprobacion


class AprobacionAdmin(admin.ModelAdmin):
    list_display = ('mac', 'distrito', 'fecha', 'calificacion')
    list_filter = ('mac', 'distrito')

    class Meta:
        fields = '__all__'
        model = Aprobacion


admin.site.register(Aprobacion, AprobacionAdmin)

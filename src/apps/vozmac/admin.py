from django.contrib import admin
from .models import PaqueteEncuesta, RespuestaEncuesta


@admin.register(PaqueteEncuesta)
class PaqueteEncuestaAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'mac', 'device_id', 'record_count', 'uploaded_at')
    search_fields = ('file_name', 'mac',)
    readonly_fields = ('file_name', 'file_hash', 'mac', 'device_id', 'record_count', 'uploaded_at')
    ordering = ('-uploaded_at',)


from django.contrib import admin
from .models import PaqueteEncuesta, RespuestaEncuesta


@admin.register(PaqueteEncuesta)
class PaqueteEncuestaAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'mac', 'device_id', 'record_count', 'uploaded_at')
    search_fields = ('file_name', 'mac',)
    readonly_fields = ('file_name', 'file_hash', 'mac', 'device_id', 'record_count', 'uploaded_at')
    ordering = ('-uploaded_at',)


@admin.register(RespuestaEncuesta)
class RespuestaEncuestaAdmin(admin.ModelAdmin):
    list_display = (
        'batch', 'created_at',
        'p0_tipo_visita', 'p1_claridad_info', 'p2_amabilidad', 'p3_instalaciones', 'p4_tiempo_espera'
    )
    list_filter = ('p0_tipo_visita', 'p1_claridad_info', 'p2_amabilidad', 'p3_instalaciones', 'p4_tiempo_espera', 'created_at')
    search_fields = ('batch__file_name',)
    readonly_fields = (
        'batch', 'created_at',
        'p0_tipo_visita', 'p1_claridad_info', 'p2_amabilidad', 'p3_instalaciones', 'p4_tiempo_espera'
    )
    ordering = ('-created_at',)

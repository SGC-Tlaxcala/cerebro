from django.contrib import admin
from .models import Plan, Accion, Seguimiento


class SeguimientoInline(admin.TabularInline):
    model = Seguimiento
    extra = 1


class AccionAdmin(admin.ModelAdmin):
    fields = (
        'plan', 'accion', 'fecha_inicio', 'fecha_fin', 'responsable',
    )
    inlines = [SeguimientoInline,]
    date_hierarchy = 'fecha_fin'
    ordering = ('fecha_fin', 'id')
    list_display = ('plan', 'fecha_inicio', 'fecha_fin', 'responsable', 'get_estado')
    list_filter = ('plan', 'seguimiento__estado', 'plan__tipo')


class AccionInline(admin.TabularInline):
    model = Accion
    extra = 1
    exclude = ('user',)  # Excluir el campo 'user'
    classes = ['collapse']  # Hacer colapsable el inline


class PlanAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identificación', {'fields': ['fecha_llenado', 'folio', 'documento', 'nombre']}),  # Identificación común
        ('Plan de Cambios y Mejoras',
         {'fields': [
             'fecha_inicio', 'fecha_termino', 'proposito', 'requisito', 'proceso', 'desc_pcm', 'consecuencias'],
          'classes': ['collapse']}),
        ('Cédula de No Conformidad',
         {'fields': ['tipo', 'desc_cnc', 'correccion', 'fuente', 'otra_fuente'],
          'classes': ['collapse']}),
        ('Análisis de la CNC o PCM', {'fields': ['analisis', 'evidencia_analisis'], 'classes': ['collapse']}),
        ('Cierre', {'fields': [
            'eliminacion',
            'txt_eliminacion',
            'recurrencia',
            'txt_recurrencia'], 'classes': ['collapse']}),
    )
    inlines = [AccionInline]

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        if obj:  # Si estamos editando un objeto existente
            if obj.documento == 1:
                # Oculta "Plan de Cambios y Mejoras" si documento == 1
                fieldsets = (
                    ('Identificación', {'fields': ['fecha_llenado', 'documento', 'nombre']}),  # Identificación común
                    ('Cédula de No Conformidad',
                     {'fields': ['tipo', 'desc_cnc', 'correccion', 'fuente', 'otra_fuente'], 'classes': ['collapse']}),
                    ('Análisis de la CNC o PCM', {'fields': ['analisis', 'evidencia_analisis'], 'classes': ['collapse']}),
                    ('Cierre', {'fields': ['eliminacion', 'txt_eliminacion', 'recurrencia', 'txt_recurrencia'], 'classes': ['collapse']}),
                )
            elif obj.documento == 2:
                # Oculta "Cédula de No Conformidad" si documento == 2
                fieldsets = (
                    ('Identificación', {'fields': ['fecha_llenado', 'documento', 'nombre']}),  # Identificación común
                    ('Plan de Cambios y Mejoras',
                     {'fields': [
                         'fecha_inicio', 'fecha_termino', 'proposito',
                         'requisito', 'proceso', 'desc_pcm', 'consecuencias'],
                      'classes': ['collapse']}),
                    ('Análisis de la CNC o PCM', {'fields': ['analisis', 'evidencia_analisis'], 'classes': ['collapse']}),
                    ('Cierre', {'fields': ['eliminacion', 'txt_eliminacion', 'recurrencia', 'txt_recurrencia'], 'classes': ['collapse']}),
                )

        return fieldsets


admin.site.register(Plan, PlanAdmin)
admin.site.register(Accion, AccionAdmin)

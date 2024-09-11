from django.contrib import admin
from django.utils.html import format_html
from .models import Plan, Accion, Seguimiento


class SeguimientoInline(admin.TabularInline):
    model = Seguimiento
    extra = 1
    exclude = ('user',)  # Excluir el campo 'user'

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)


class AccionAdmin(admin.ModelAdmin):
    fields = ('plan', 'accion', 'fecha_inicio', 'fecha_fin', 'responsable')
    inlines = [SeguimientoInline,]
    date_hierarchy = 'fecha_fin'
    ordering = ('fecha_fin', 'id')
    list_display = ('plan', 'fecha_inicio', 'fecha_fin', 'responsable', 'get_estado')
    list_filter = ('plan', 'seguimiento__estado', 'plan__tipo')

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = request.user
            instance.save()
        formset.save_m2m()

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        for formset in formsets:
            for obj in formset.save(commit=False):
                if isinstance(obj, Accion) and not obj.user_id:
                    obj.user = request.user
                    obj.save()


class AccionInline(admin.TabularInline):
    model = Accion
    extra = 1
    exclude = ('user',)
    fields = ('accion', 'responsable', 'recursos', 'evidencia', 'fecha_inicio', 'fecha_fin', 'edit_link')
    readonly_fields = ('edit_link',)
    classes = ['collapse']

    def edit_link(self, obj):
        if obj.id:  # Asegúrate de que el objeto tiene un ID antes de generar el enlace
            return format_html('<a class="changelink" href="/admin/pas/accion/{}/change/">&nbsp;</a>', obj.id)
        return "-"
    edit_link.short_description = 'Seg'
    edit_link.allow_tags = True

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)


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
            'eliminacion', 'txt_eliminacion',
            'recurrencia', 'txt_recurrencia'], 'classes': ['collapse']}),
    )
    inlines = [AccionInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = request.user
            instance.save()
        formset.save_m2m()

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        for formset in formsets:
            for obj in formset.save(commit=False):
                if isinstance(obj, Accion) and not obj.user_id:
                    obj.user = request.user
                    obj.save()

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        if obj:  # Si estamos editando un objeto existente
            if obj.documento == 1:
                # Oculta "Plan de Cambios y Mejoras" si documento == 1
                fieldsets = (
                    ('Identificación', {'fields': ['fecha_llenado', 'folio', 'documento', 'nombre']}),  # Identificación común
                    ('Cédula de No Conformidad',
                     {'fields': ['tipo', 'desc_cnc', 'correccion', 'fuente', 'otra_fuente'], 'classes': ['collapse']}),
                    ('Análisis de la Cédula de No Conformidad',
                     {'fields': ['analisis', 'evidencia_analisis'], 'classes': ['collapse']}),
                    ('Cierre',
                     {'fields': ['eliminacion', 'txt_eliminacion', 'recurrencia', 'txt_recurrencia'],
                      'classes': ['collapse']}),
                )
            elif obj.documento == 2:
                # Oculta "Cédula de No Conformidad" si documento == 2
                fieldsets = (
                    ('Identificación', {'fields': ['fecha_llenado', 'folio', 'documento', 'nombre']}),  # Identificación común
                    ('Plan de Cambios y Mejoras',
                     {'fields': [
                         'fecha_inicio', 'fecha_termino', 'proposito',
                         'requisito', 'proceso', 'desc_pcm', 'consecuencias'],
                      'classes': ['collapse']}),
                    ('Análisis del Plan de Cambios y Mejoras',
                     {'fields': ['analisis', 'evidencia_analisis'], 'classes': ['collapse']}),
                    ('Cierre',
                     {'fields': ['eliminacion', 'txt_eliminacion', 'recurrencia', 'txt_recurrencia'],
                      'classes': ['collapse']}),
                )

        return fieldsets


admin.site.register(Plan, PlanAdmin)
admin.site.register(Accion, AccionAdmin)

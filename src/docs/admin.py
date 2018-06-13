from django.contrib import admin
from django import forms
from docs.models import Tipo, Proceso, Documento, Revision


class DocumentAdminForm (forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Documento
        texto_ayuda = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    'class': 'mceEditor vLargeTextField',
                    'rows': 4,
                }
            )
        )


class TipoAdmin (admin.ModelAdmin):
    prepopulated_fields = {"slug": ("tipo",)}


class ProcesoAdmin (admin.ModelAdmin):
    prepopulated_fields = {"slug": ("proceso",)}


class RevisionInline (admin.TabularInline):
    model = Revision
    extra = 1


class DocumentoAdmin (admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nombre",)}
    list_display = ('nombre', 'proceso', 'tipo', 'activo')
    list_filter = ['proceso', 'tipo', 'activo']
    form = DocumentAdminForm
    inlines = [RevisionInline]

    def save_model(self, request, obj, form, change):
        obj.autor = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.autor = request.user
            instance.save()
        formset.save_m2m()


class RevisionAdmin (admin.ModelAdmin):
    list_filter = ['documento']
    fieldsets = [
        (None, {'fields': ['revision', 'f_actualizacion']}),
        ('Control de Cambios', {'fields': ['cambios'], 'classes': ['collapse']}),
    ]

    def save_model(self, request, obj, form, change):
        obj.autor = request.user
        obj.save()


admin.site.register(Tipo, TipoAdmin)
admin.site.register(Proceso, ProcesoAdmin)
admin.site.register(Documento, DocumentoAdmin)

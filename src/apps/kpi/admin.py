from django.contrib import admin
from django.contrib.admin import TabularInline

from .models import KPI, Record

class RecordInline(TabularInline):
    model = Record
    extra = 1

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(KPI)
class KPIAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'period', 'target', 'active')
    search_fields = ('name', 'description')
    list_filter = ('type', 'period', 'active')
    ordering = ('pos',)
    inlines = [RecordInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        for formset in formsets:
            if isinstance(formset, RecordInline):
                for obj in formset.save(commit=False):
                    if not obj.pk:
                        obj.user = request.user
                    obj.save()


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('kpi', 'date', 'value')
    search_fields = ('kpi__name',)
    list_filter = ('kpi', 'date')
    ordering = ('kpi', 'date')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)



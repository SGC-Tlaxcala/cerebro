from django.contrib import admin
from django.contrib.admin import TabularInline

from .models import KPI, Record, Period

class RecordInline(TabularInline):
    exclude = ('user',)
    model = Record
    extra = 1

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)


class PeriodInline(TabularInline):
    exclude = ('user',)
    model = Period
    extra = 1

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(KPI)
class KPIAdmin(admin.ModelAdmin):
    exclude = ('user',)
    list_display = ('name', 'type', 'active')
    search_fields = ('name', 'description')
    list_filter = ('type', 'active')
    ordering = ('pos',)
    inlines = [PeriodInline]

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        for formset in formsets:
            if isinstance(formset, PeriodInline):
                for obj in formset.save(commit=False):
                    if not obj.pk:
                        obj.user = request.user
                    obj.save()


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    exclude = ('user',)
    list_display = ('period', 'date', 'value')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)



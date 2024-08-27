from django.contrib import admin
from django.utils.html import mark_safe
from .models import Idea, Resolve


class ResolveAdminInline(admin.TabularInline):
    model = Resolve
    extra = 0


class ResolveAdmin(admin.ModelAdmin):
    list_display = ('idea', 'user', 'resolve', 'viable')
    list_filter = ('idea', 'author')
    search_fields = ('viable', 'idea')

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


class IdeaAdmin(admin.ModelAdmin):
    list_display = ('type', 'scope', 'title', 'viable', 'state')
    list_filter = ('type', 'scope')
    search_fields = ('desc', 'results', 'title')
    inlines = [ResolveAdminInline]


    def viable(self, obj):
        viable = '<strong>Sí</strong>' if obj.resolve_set.last().viable else '<i>No</i>'
        return mark_safe(f'{viable}')

    def state(self, obj):
        return mark_safe(f'{obj.resolve_set.last().resolve}')

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.autor = request.user
            instance.save()
        formset.save_m2m()


admin.site.register(Idea, IdeaAdmin)

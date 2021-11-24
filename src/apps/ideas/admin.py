from django.contrib import admin
from .models import Idea


class IdeaAdmin(admin.ModelAdmin):
    list_display = ('type', 'scope', 'desc')
    list_filter = ('type', 'scope')
    search_fields = ('desc', 'results')


admin.site.register(Idea, IdeaAdmin)

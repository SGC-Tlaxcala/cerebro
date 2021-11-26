from django.contrib import admin
from .models import Idea


class IdeaAdmin(admin.ModelAdmin):
    list_display = ('type', 'scope', 'title')
    list_filter = ('type', 'scope')
    search_fields = ('desc', 'results', 'title')


admin.site.register(Idea, IdeaAdmin)

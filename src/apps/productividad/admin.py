# coding: utf-8
"""Área administrativa de productividad."""

from django.contrib import admin
from apps.productividad.models import PronosticoTramites


class PronosticoTramitesAdmin(admin.ModelAdmin):
    """Generador simple de administración del modelo"""
    pass


admin.site.register(PronosticoTramites, PronosticoTramitesAdmin)

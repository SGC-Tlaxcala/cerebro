"""Librería de etiquetas personalizadas para el sistema PAS."""

from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def pas_color(documento):
    """Devuelve el color de un documento."""
    if documento == 1:
        return 'danger'
    else:
        return 'primary'

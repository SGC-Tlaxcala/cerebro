"""Librería de etiquetas personalizadas para el sistema PAS."""

from django import template


register = template.Library()


@register.simple_tag
def pas_color(documento):
    """Devuelve el color de un documento."""
    if documento == 1:
        return 'danger'
    else:
        return 'primary'


@register.filter(name='pas_icon')
def pas_icon(documento):
    """Devuelve el tipo de un plan de acción."""
    if documento == 1:
        return 'bug'
    elif documento == 2:
        return 'thumbs-o-up'

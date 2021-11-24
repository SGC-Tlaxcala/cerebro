from django.db import models
from tinymce.models import HTMLField


IDEA = 0
PROJECT = 1
TYPE = (
    (IDEA, 'Idea'),
    (PROJECT, 'Proyecto')
)

PROCESS = 0
ACTIVITY = 1
SYSTEM = 2
FORMAT = 3
KPI = 4
GOAL = 5
SCOPE = (
    (PROCESS, 'Proceso'),
    (ACTIVITY, 'Actividad'),
    (SYSTEM, 'Sistema'),
    (FORMAT, 'Formato'),
    (KPI, 'Indicador'),
    (GOAL, 'Objetivo')
)


class Idea(models.Model):
    type = models.PositiveSmallIntegerField(
        'Tipo',
        choices=TYPE,
        help_text='Selecciona si presentas una idea o un proyecto')
    scope = models.PositiveSmallIntegerField(
        'Alcance',
        choices=SCOPE,
        default=PROCESS,
        help_text='Selecciona que vas a afectar con tu idea')
    name = models.CharField(
        'Nombre', max_length=120,
        help_text='Escribe tu nombre')
    contact = models.CharField(
        'Contacto', max_length=100,
        help_text='Escribe tu correo electrónico o número telefónico')
    site = models.CharField(
        'Sitio', max_length=30,
        help_text='Escribe tu módulo o Junta')
    desc = HTMLField(
        'Descripción',
        help_text='''Escribe tu idea o proyecto. Un proyecto es algo que quieres
        implementar. Describe qué quieres lograr y cómo quieres lograrlo''')
    results = HTMLField(
        'Results', blank=True, null=True,
        help_text='Escribe los resultados que has obtenido con tu proyecto')
    docs = models.FileField(
        'Formatos', upload_to='ideas', blank=True, null=True,
        help_text='Sube los formatos que uses en tu proyecto en un solo zip')
    evidence = models.FileField(
        'Evidencias', upload_to='ideas', blank=True, null=True,
        help_text='Sube las evidencias que usaste en tu proyecto en un solo zip')

    def __str__(self):
        return f'idea-{self.id}'

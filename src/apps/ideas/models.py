from django.db import models
from django.utils.text import slugify
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
CMI = 6
SCOPE = (
    (PROCESS, 'Proceso'),
    (ACTIVITY, 'Actividad'),
    (SYSTEM, 'Sistema'),
    (FORMAT, 'Formato'),
    (KPI, 'Indicador'),
    (GOAL, 'Objetivo'),
    (CMI, 'Cuadro de Mando')
)


class Idea(models.Model):
    title = models.CharField('Título', max_length=200)
    slug = models.SlugField('Slug', max_length=200, unique=True, editable=False)
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
        help_text='Escribe tu correo electrónico institucional')
    site = models.CharField(
        'Sitio', max_length=30,
        help_text='Escribe tu módulo o Junta')
    desc = HTMLField(
        'Descripción',
        help_text='''Escribe tu idea o proyecto. Un proyecto es algo que quieres
        implementar. Describe qué quieres lograr y cómo quieres lograrlo''')
    results = HTMLField(
        'Resultados', blank=True, null=True,
        help_text='Escribe los resultados que has obtenido con tu proyecto')
    docs = models.FileField(
        'Formatos', upload_to='ideas', blank=True, null=True,
        help_text='Sube los formatos que uses en tu proyecto en un solo zip')
    evidence = models.FileField(
        'Evidencias', upload_to='ideas', blank=True, null=True,
        help_text='Sube las evidencias que usaste en tu proyecto en un solo zip')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Idea, self).save(*args, **kwargs)

    def __str__(self):
        return f'idea-{self.id}'

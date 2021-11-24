from django.db import models


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
    type = models.PositiveSmallIntegerField('Tipo', choices=TYPE)
    scope = models.PositiveSmallIntegerField('Alcance', choices=SCOPE, default=PROCESS)
    name = models.CharField('Nombre', max_length=120)
    contact = models.CharField('Contacto', max_length=100)
    site = models.CharField('Sitio', max_length=30)
    desc = models.TextField('Descripción')
    results = models.TextField('Results', blank=True, null=True)
    docs = models.FileField(upload_to='ideas', blank=True, null=True)
    evidence = models.FileField(upload_to='ideas', blank=True, null=True)

    def __str__(self):
        return f'idea-{self.id}'

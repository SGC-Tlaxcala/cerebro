from django.db import models


MODULOS = (
    ('290151', '290151'),
    ('290152', '290152'),
    ('290153', '290153'),
    ('290251', '290251'),
    ('290252', '290252'),
    ('290253', '290253'),
    ('290254', '290254'),
    ('290351', '290351'),
    ('290352', '290352'),
    ('290353', '290353')
)


class Aprobacion(models.Model):
    mac = models.CharField('Módulo', max_length=6, choices=MODULOS)
    distrito = models.PositiveSmallIntegerField('Distrito', editable=False)
    fecha = models.DateField('Fecha')
    calificacion = models.FloatField('Calificación')
    nota = models.TextField()

    def __str__(self):
        return f'{self.mac} - {self.fecha.strftime("%Y-%m")}'

    def save(self, *args, **kwargs):
        self.distrito = self.mac[3]
        super(Aprobacion, self).save(*args, **kwargs)

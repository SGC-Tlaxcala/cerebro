from django.db import models


class Cobertura(models.Model):
    fecha = models.DateField('mes', help_text='Seleccione el último día del mes')
    padron = models.PositiveIntegerField('Padrón Electoral')
    lista = models.PositiveIntegerField('Lista Nominal')
    diferencia = models.IntegerField('Diferencia', editable=False)
    cob = models.FloatField('Cobertura', editable=False)

    def __str__(self):
        return f'{self.fecha.strftime("%Y-%m")}: {"{:.2%}".format(self.cob)}'

    def save(self, *args, **kwargs):
        self.diferencia = self.padron - self.lista
        self.cob = float(self.lista) / float(self.padron)
        super(Cobertura, self).save(*args, **kwargs)

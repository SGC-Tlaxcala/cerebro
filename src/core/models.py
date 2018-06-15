# coding: utf-8
#         app: cerebro
#      module: core.models
#        date: lunes, 28 de mayo de 2018 - 13:16
# description: Modelos de comportamiento comunes
# pylint: disable=W0613,R0201,R0903


from django.db import models


class TimeStampedModel(models.Model):
    """
    Una clase abstracta que sirve de base para modelos.
    Actualiza automáticamente los campos ``creado`` y ``modificado``.
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Remesa (models.Model):
    remesa = models.CharField(max_length=7)
    inicio = models.DateField()
    fin = models.DateField()

    def days(self):
        return self.fin - self.inicio

    def __str__(self):
        return f"Remesa {self.remesa}"

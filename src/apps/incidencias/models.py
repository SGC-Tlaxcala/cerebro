from django.db import models

# Create your models here.

class Tipo(models.Model):
    nombre = models.CharField(max_length=255)

class Incidencia(models.Model):
    distrito = models.PositiveSmallIntegerField()
    modulo = models.CharField(max_length=6)
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    inhabilitado = models.BooleanField()
    caso_cau = models.CharField(max_length=15)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    descripcion = models.TextField()
    solucion = models.TextField()

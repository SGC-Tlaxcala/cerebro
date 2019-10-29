# Generated by Django 2.2.6 on 2019-10-29 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('fecha', models.DateField(verbose_name='Fecha')),
                ('remesa', models.CharField(editable=False, max_length=7, null=True, verbose_name='Remesa')),
                ('distrito', models.PositiveSmallIntegerField(editable=False, verbose_name='Distrito')),
                ('modulo', models.CharField(max_length=3, verbose_name='Módulo')),
                ('lugar', models.PositiveSmallIntegerField(choices=[(1, 'Barra: Área de Trámite/Entrega'), (2, 'Mesa: Mesa de atención')], verbose_name='Lugar de atención')),
                ('sexo', models.CharField(choices=[('H', 'Hombre'), ('M', 'Mujer')], max_length=1, verbose_name='Sexo')),
                ('causa', models.PositiveSmallIntegerField(choices=[(1, '1. Falta el acta de nacimiento'), (2, '2. Falta identificación'), (3, '3. Falta comprobante de domicilio'), (4, '4. Solo necesita información'), (5, '5. Va a recoger su CPV'), (6, '6. No hay mas fichas'), (7, '7. Menor de 18 años'), (8, '8. No pasó la huella'), (9, '9. Otra causa')], verbose_name='Causa')),
                ('observaciones', models.TextField(blank=True, null=True, verbose_name='Observaciones')),
            ],
            options={
                'verbose_name': 'Registro de Atención',
                'verbose_name_plural': 'Registros de Atención',
            },
        ),
    ]

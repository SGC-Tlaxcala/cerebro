# Generated by Django 2.1.7 on 2019-03-11 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidencias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='modulo',
            name='tipo_mac',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Fijo Distrital'), (2, 'Fijo Adicional'), (3, 'Semifijo'), (4, 'Móvil')], default=1),
            preserve_default=False,
        ),
    ]

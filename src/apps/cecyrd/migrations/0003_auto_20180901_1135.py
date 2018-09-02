# Generated by Django 2.1 on 2018-09-01 16:35

from django.db import migrations, models
from datetime import timedelta


class Migration(migrations.Migration):

    dependencies = [
        ('cecyrd', '0002_auto_20180901_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='tramites',
            name='tramo_disponible',
            field=models.DurationField(default=timedelta(seconds=0), editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tramites',
            name='tramo_entrega',
            field=models.DurationField(default=timedelta(seconds=0), editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tramites',
            name='tramo_exitoso',
            field=models.DurationField(default=timedelta(seconds=0), editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tramites',
            name='distrito',
            field=models.PositiveSmallIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='tramites',
            name='mac',
            field=models.CharField(editable=False, max_length=6),
        ),
    ]

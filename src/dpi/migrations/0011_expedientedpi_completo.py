# Generated by Django 2.0.5 on 2018-06-18 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpi', '0010_remove_expedientedpi_completo'),
    ]

    operations = [
        migrations.AddField(
            model_name='expedientedpi',
            name='completo',
            field=models.PositiveSmallIntegerField(default=0, editable=False),
        ),
    ]
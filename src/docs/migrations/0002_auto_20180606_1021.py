# Generated by Django 2.0.5 on 2018-06-06 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documento',
            old_name='updated',
            new_name='actualiza',
        ),
        migrations.RenameField(
            model_name='documento',
            old_name='created',
            new_name='creacion',
        ),
        migrations.RenameField(
            model_name='revision',
            old_name='updated',
            new_name='actualiza',
        ),
        migrations.RenameField(
            model_name='revision',
            old_name='created',
            new_name='creacion',
        ),
    ]
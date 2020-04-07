# Generated by Django 3.0.4 on 2020-04-07 17:28

import apps.metas.models
from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=2, verbose_name='Clave de la Meta')),
                ('name', models.CharField(max_length=25, verbose_name='Identificación')),
                ('year', models.PositiveIntegerField(verbose_name='Año')),
                ('cicles', models.PositiveSmallIntegerField(verbose_name='Repeticiones')),
                ('description', models.TextField(verbose_name='Descripción de la Meta')),
                ('support', models.FileField(blank=True, null=True, upload_to=apps.metas.models.archivo_soporte, verbose_name='Soporte')),
                ('fields', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Meta',
                'verbose_name_plural': 'Control de Metas del SPE',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('mail', models.CharField(max_length=50, verbose_name='Correo Electrónico')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('clave', models.CharField(max_length=7, verbose_name='Clave del Puesto')),
                ('description', models.CharField(max_length=75, verbose_name='Descripción')),
                ('order', models.PositiveSmallIntegerField(verbose_name='Orden')),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('site', models.CharField(max_length=4, verbose_name='Sitio')),
                ('name', models.CharField(default='', max_length=50, verbose_name='Nombre')),
                ('address', models.CharField(max_length=100, verbose_name='Dirección')),
            ],
        ),
        migrations.CreateModel(
            name='Proof',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('fields', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proof_goal', to='metas.Goal')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proof_member', to='metas.Member', verbose_name='Miembro del SPE')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='evidencia_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Evidencia',
                'verbose_name_plural': 'Evidencias',
            },
        ),
        migrations.AddField(
            model_name='member',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_role', to='metas.Role', verbose_name='Puesto'),
        ),
        migrations.AddField(
            model_name='member',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_site', to='metas.Site', verbose_name='Sitio'),
        ),
        migrations.AddField(
            model_name='goal',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goal_role', to='metas.Role'),
        ),
        migrations.AddField(
            model_name='goal',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='goal_user', to=settings.AUTH_USER_MODEL),
        ),
    ]

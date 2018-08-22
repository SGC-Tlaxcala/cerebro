# Generated by Django 2.1 on 2018-08-10 04:30

from django.conf import settings
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
            name='ExpedienteDPI',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tipo', models.CharField(choices=[('DPI', 'Datos Personales Irregulares'), ('USI', 'Usurpación de Identidad')], max_length=3)),
                ('folio', models.CharField(max_length=13)),
                ('nombre', models.CharField(max_length=100)),
                ('fecha_tramite', models.DateField(blank=True, null=True)),
                ('fecha_notificacion_aclaracion', models.DateField(blank=True, help_text='Fecha de notificación de aclaración al ciudadano AC', null=True, verbose_name='TRÁMITE: Notificación')),
                ('fecha_entrevista', models.DateField(blank=True, help_text='TRÁMITE: Fecha de la entrevista o Acta Administrativa', null=True)),
                ('fecha_envio_expediente', models.DateField(blank=True, help_text='TRÁMITE: Fecha de envío de expediente a la JL', null=True)),
                ('fecha_notificacion_registro', models.DateField(blank=True, help_text='Fecha de notificación de aclaración al ciudadano AC', null=True, verbose_name='REGISTRO: Notificación')),
                ('fecha_entrevista_registro', models.DateField(blank=True, help_text='Fecha de la entrevista o Acta Administrativa', null=True, verbose_name='REGISTRO: Entrevista/Acta')),
                ('fecha_envio_expediente_registro', models.DateField(blank=True, help_text='REGISTRO: Fecha de envío de expediente a la JL', null=True, verbose_name='REGISTRO: Envio a JL')),
                ('fecha_solicitud_cedula', models.DateField(blank=True, help_text='Fecha de solicitud de cédula', null=True)),
                ('fecha_ejecucion_cedula', models.DateField(blank=True, help_text='Fecha de ejecución de la cédula', null=True)),
                ('fecha_validacion_expediente', models.DateField(blank=True, help_text='Fecha de validación de expediente', null=True)),
                ('estado', models.PositiveSmallIntegerField(choices=[(0, 'No indica'), (1, 'Rechazado'), (2, 'Error en MAC'), (3, 'Aclarado')], default=0, help_text='Estado del trámite')),
                ('fecha_notificacion_rechazo', models.DateField(blank=True, help_text='Fecha de notificación de trámite rechazado RE', null=True)),
                ('fecha_notificacion_exclusion', models.DateField(blank=True, help_text='Fecha de notificación de exclusión de registro', null=True)),
                ('entidad', models.PositiveSmallIntegerField(editable=False, help_text='Entidad')),
                ('distrito', models.PositiveSmallIntegerField(editable=False, help_text='Distrito')),
                ('delta_notificar', models.SmallIntegerField(editable=False, help_text='Delta entre tramite y notificación', null=True)),
                ('delta_aclarar', models.SmallIntegerField(editable=False, help_text='Delta entre notificación y entrevista', null=True)),
                ('delta_entrevista', models.SmallIntegerField(editable=False, help_text='Delta entre notificación y entrevista', null=True)),
                ('delta_enviar', models.SmallIntegerField(editable=False, help_text='Delta entre entrevista y envío a JL', null=True)),
                ('delta_distrito', models.SmallIntegerField(editable=False, help_text='Delta entre tramite y envío a JL', null=True)),
                ('delta_verificar', models.SmallIntegerField(editable=False, help_text='Delta entre solicitud de verificación y ejecución de la cédula', null=True)),
                ('completo', models.PositiveSmallIntegerField(default=0, editable=False)),
                ('usuario', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='dpi_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Expediente DPI',
                'verbose_name_plural': 'Expedientes de DPI',
                'ordering': ['-fecha_tramite'],
            },
        ),
        migrations.AddIndex(
            model_name='expedientedpi',
            index=models.Index(fields=['folio'], name='folio_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='expedientedpi',
            unique_together={('tipo', 'folio')},
        ),
    ]
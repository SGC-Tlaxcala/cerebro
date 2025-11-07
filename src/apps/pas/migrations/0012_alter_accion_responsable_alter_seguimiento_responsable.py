from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def normalize_responsables(apps, schema_editor):
    Accion = apps.get_model('pas', 'Accion')
    Seguimiento = apps.get_model('pas', 'Seguimiento')
    app_label, model_name = settings.AUTH_USER_MODEL.split('.')
    User = apps.get_model(app_label, model_name)

    def build_lookup():
        lookup = {}

        def add_key(key, user):
            if not key:
                return
            normalized = key.strip().lower()
            if normalized and normalized not in lookup:
                lookup[normalized] = user

        for user in User.objects.all():
            add_key(str(user.pk), user)
            add_key(user.username, user)
            add_key(user.email, user)
            if user.email and '@' in user.email:
                add_key(user.email.split('@')[0], user)
            full_name = f'{user.first_name} {user.last_name}'.strip()
            add_key(full_name, user)
        return lookup

    lookup = build_lookup()

    def resolve(value):
        if not value:
            return None
        key = value.strip().lower()
        if not key:
            return None
        user = lookup.get(key)
        if not user and '@' in key:
            user = lookup.get(key.split('@')[0])
        return user

    def assign_responsable(instance, attr):
        raw_value = getattr(instance, attr, '')
        if raw_value is None:
            raw_value = ''
        value = str(raw_value).strip()
        user = resolve(value)
        if user:
            setattr(instance, attr, str(user.pk))
        else:
            setattr(instance, attr, None)
        instance.save(update_fields=[attr])

    for accion in Accion.objects.all():
        assign_responsable(accion, 'responsable')

    for seguimiento in Seguimiento.objects.all():
        assign_responsable(seguimiento, 'responsable')


class Migration(migrations.Migration):

    dependencies = [
        ('pas', '0011_alter_seguimiento_responsable'),
    ]

    operations = [
        migrations.RunPython(normalize_responsables, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='accion',
            name='responsable',
            field=models.ForeignKey(
                blank=True,
                help_text='Persona responsable de la actividad',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='acciones_responsables',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name='seguimiento',
            name='responsable',
            field=models.ForeignKey(
                blank=True,
                help_text='Persona responsable de la actualización',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='seguimientos_responsables',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

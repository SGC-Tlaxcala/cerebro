import os
import requests
import logging
import pytz

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone

from apps.docs.models import Revision, Notificacion
from apps.profiles.models import Profile

logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.WARNING)

class Command(BaseCommand):
    help = 'Envía notificaciones programadas para revisiones de documentos no urgentes.'

    def handle(self, *args, **options):
        tz = pytz.timezone('America/Mexico_City')
        ahora = timezone.now().astimezone(tz)

        revisiones_pendientes = Revision.objects.filter(notificacion_enviada=False)

        if not revisiones_pendientes.exists():
            self.stdout.write(self.style.SUCCESS(
                f"[{ahora.strftime('%Y-%m-%d %H:%M')}] No hay revisiones pendientes de notificación."))
            return

        destinatarios = Profile.objects.filter(recibe_notificaciones=True, user__email__isnull=False)

        if not destinatarios.exists():
            self.stdout.write(self.style.WARNING(f"[{ahora.strftime('%Y-%m-%d %H:%M')}] No se encontraron destinatarios para las notificaciones."))
            return

        context = {
            'revisiones': revisiones_pendientes,
            'fecha_notificacion': ahora.strftime('%d/%b/%Y'),
        }

        asunto = f"Documentos actualizados a la fecha {context['fecha_notificacion']}"
        mensaje_html = render_to_string('docs/notificacion_periodica.html', context)

        api_key = os.getenv('EMAIL_API_KEY')
        from_email = 'Cerebro <cerebro@sgctlaxcala.com.mx>'

        if not api_key:
            logger.critical(f"[{ahora.strftime('%Y-%m-%d %H:%M')}] No se encontró la variable de entorno EMAIL_API_KEY. No se pueden enviar notificaciones.")
            self.stdout.write(self.style.ERROR('Error: EMAIL_API_KEY no configurada.'))
            return

        for destinatario_profile in destinatarios:
            nombre_usuario = destinatario_profile.user.get_full_name()
            if not nombre_usuario:
                nombre_usuario = destinatario_profile.user.username or destinatario_profile.user.email.split('@')[0]

            to_email = f"{nombre_usuario} <{destinatario_profile.user.email}>"

            try:
                response = requests.post(
                    "https://api.mailgun.net/v3/sgctlaxcala.com.mx/messages",
                    auth=("api", api_key),
                    data={
                        "from": from_email,
                        "to": to_email,
                        "subject": asunto,
                        "html": mensaje_html
                    }
                )
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                logger.error(f"[{ahora.strftime('%Y-%m-%d %H:%M')}] Error al enviar notificación a {destinatario_profile.user.email}: {e}")
                self.stdout.write(self.style.ERROR(f'Error al enviar notificación a {destinatario_profile.user.email}: {e}'))

        for revision in revisiones_pendientes:
            revision.fecha_notificacion = ahora
            revision.notificacion_enviada = True
            revision.save()

        cuerpo_html_para_notificacion = render_to_string('docs/notificacion_periodica_content.html', context)
        Notificacion.objects.create(
            documento=None,
            revision_obj=None,
            destinatarios=", ".join([p.user.email for p in destinatarios if p.user.email]),
            tipo='P',
            asunto=asunto,
            cuerpo_html=cuerpo_html_para_notificacion,
        )

        self.stdout.write(self.style.SUCCESS(f"[{ahora.strftime('%Y-%m-%d %H:%M')}] Notificaciones programadas enviadas a {destinatarios.count()} destinatarios."))

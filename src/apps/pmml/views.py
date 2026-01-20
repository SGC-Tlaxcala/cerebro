import os
import requests
import uuid
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from .models import Subscriber
from .forms import SubscriptionForm

logger = logging.getLogger(__name__)


def register(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscriber = form.save(commit=False)
            subscriber.token = uuid.uuid4()
            subscriber.is_active = False
            subscriber.save()

            # Enviar correo de activación
            send_activation_email(subscriber, request)

            messages.success(
                request,
                f"Gracias por registrarte, {subscriber.nombre_completo}. Revisa tu correo ({subscriber.email_full}) para activar tu suscripción.",
            )
            return redirect("pmml:register")
    else:
        form = SubscriptionForm()

    return render(request, "pmml/signup.html", {"form": form})


def verify(request, token):
    subscriber = get_object_or_404(Subscriber, token=token)
    if not subscriber.is_active:
        subscriber.is_active = True
        subscriber.save()
        messages.success(request, "¡Tu suscripción ha sido activada correctamente!")
    else:
        messages.info(request, "Tu suscripción ya estaba activa.")

    return render(request, "pmml/verify.html")


def send_activation_email(subscriber, request):
    api_key = os.getenv("EMAIL_API_KEY")
    if not api_key:
        logger.error(
            "EMAIL_API_KEY no configurada. No se pudo enviar el correo de activación."
        )
        return

    # Construir link de activación con IP fija según requerimiento
    # "http://10.29.0.35/pmml/verify/<token>/"
    # Usamos reverse para obtener la ruta relativa y concatenamos
    relative_path = reverse("pmml:verify", args=[subscriber.token])
    activation_link = f"http://10.29.0.35{relative_path}"

    from_email = "Cerebro <cerebro@cmi.lat>"
    to_email = f"{subscriber.nombre_completo} <{subscriber.email_full}>"
    subject = "Confirma tu suscripción a Notificaciones CMI"

    html_content = f"""
    <p>Hola {subscriber.nombre_completo},</p>
    <p>Para recibir las notificaciones de documentos del sistema CMI, por favor confirma tu suscripción haciendo clic en el siguiente enlace:</p>
    <p><a href="{activation_link}">Activar Suscripción</a></p>
    <p>Si no solicitaste esto, puedes ignorar este correo.</p>
    <p>Saludos,<br>Equipo CMI</p>
    """

    try:
        response = requests.post(
            "https://api.mailgun.net/v3/cmi.lat/messages",
            auth=("api", api_key),
            data={
                "from": from_email,
                "to": to_email,
                "subject": subject,
                "html": html_content,
                "text": f"Hola {subscriber.nombre_completo}, confirma tu suscripción en: {activation_link}",
            },
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error al enviar correo a {to_email}: {e}")

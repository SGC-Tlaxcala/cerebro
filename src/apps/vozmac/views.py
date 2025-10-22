import os
import hashlib
import gzip
import logging
import json
from datetime import datetime, timedelta
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Avg, Count
from django.db.models.functions import TruncMonth
from django.conf import settings
from django.contrib import messages
from .forms import SurveyBatchForm
from .models import PaqueteEncuesta, RespuestaEncuesta


logger = logging.getLogger(__name__)


def obtener_datos_paquete(file_path, file_name):
    """
    Procesa el archivo .gz subido y extrae los datos necesarios para PaqueteEncuesta.
    """
    # Extraer mac y device_id del nombre
    base = file_name.split('.')[0]  # vozMAC-290421-A-20251013-135803
    partes = base.split('-')
    mac = partes[1]
    device_id = partes[2]

    # Leer y descomprimir archivo
    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
        contenido = f.read()
        respuestas = contenido.strip().split('\n')
        record_count = len(respuestas)
        file_hash = hashlib.sha256(contenido.encode('utf-8')).hexdigest()

    return {
        'file_name': file_name,
        'file_hash': file_hash,
        'mac': mac,
        'device_id': device_id,
        'record_count': record_count,
        'respuestas': respuestas
    }


def _parse_device_id(device_id):
    digits = ''.join(ch for ch in (device_id or '') if ch.isdigit())
    entidad = int(digits[0:2]) if len(digits) >= 2 else None
    distrito = int(digits[2:4]) if len(digits) >= 4 else None
    mac = digits[:6] if len(digits) >= 1 else None
    return entidad, distrito, mac


def insertar_respuestas(paquete, respuestas):
    respuestas_para_procesar = []
    try:
        for respuesta_json in respuestas:
            if not respuesta_json:
                continue
            datos = json.loads(respuesta_json)
            device = datos.get('device_id')
            entidad, distrito, mac = _parse_device_id(device)

            datos.pop('device_id', None)
            datos.pop('is_exported', None)

            instancia = RespuestaEncuesta(batch=paquete, **datos)
            if entidad is not None:
                instancia.entidad = entidad
            if distrito is not None:
                instancia.distrito = distrito
            if mac is not None:
                instancia.mac = mac

            respuestas_para_procesar.append(instancia)

        if respuestas_para_procesar:
            RespuestaEncuesta.objects.bulk_create(respuestas_para_procesar)
            logger.info(f"Se insertaron {len(respuestas_para_procesar)} respuestas del paquete {paquete.id}")
    except json.JSONDecodeError as e:
        logger.error(f"Error al decodificar el paquete {paquete.id}: {e}")
    except Exception as e:
        logger.error(f"Error inesperado al procesar el paquete {paquete.id}: {e}")


class VozMACAdd(TemplateView):
    template_name = 'vozmac/add.html'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['form'] = kwargs.get('form', SurveyBatchForm())
        contexto['cargas_recientes'] = PaqueteEncuesta.objects.order_by('-uploaded_at')[:20]
        return contexto

    def post(self, request, *args, **kwargs):
        form = SurveyBatchForm(request.POST, request.FILES)
        if not form.is_valid():
            messages.error(request, "Formulario inválido")
            return render(request, self.template_name, self.get_context_data(form=form))

        try:
            # Obtener archivo subido (si existe)
            file_field = next(iter(request.FILES), None)
            uploaded = request.FILES[file_field] if file_field else None
            paquete = None
            respuestas = None

            if uploaded:
                tmp_dir = os.path.join(settings.MEDIA_ROOT, 'vozmac_tmp')
                os.makedirs(tmp_dir, exist_ok=True)
                tmp_path = os.path.join(tmp_dir, uploaded.name)

                # Guardar temporalmente
                with open(tmp_path, 'wb') as f:
                    for chunk in uploaded.chunks():
                        f.write(chunk)

                # Extraer metadatos y respuestas
                datos = obtener_datos_paquete(tmp_path, uploaded.name)

                # Crear registro mínimo de paquete; asignar metadatos si existen como atributos
                paquete = PaqueteEncuesta.objects.create(file_name=datos.get('file_name', uploaded.name))
                for key in ('file_hash', 'mac', 'device_id', 'record_count'):
                    if key in datos:
                        try:
                            setattr(paquete, key, datos[key])
                        except Exception:
                            pass
                try:
                    paquete.save()
                except Exception:
                    # Si algunos campos no existen en el modelo, seguimos sin fallar
                    logger.debug("No se pudieron guardar algunos metadatos del paquete; continuando.")

                respuestas = datos.get('respuestas')

            # Si el formulario trae respuestas directamente (campo del formulario)
            if not respuestas:
                respuestas = form.cleaned_data.get('respuestas') if hasattr(form, 'cleaned_data') else None

            insertar_respuestas(paquete, respuestas or [])
            messages.success(request, "Paquete procesado correctamente")
            return render(request, self.template_name, self.get_context_data(form=SurveyBatchForm()))
        except Exception as e:
            logger.exception("Error al procesar el paquete")
            messages.error(request, f"Error al procesar: {e}")
            return render(request, self.template_name, self.get_context_data(form=form))


class VozMACIndex(TemplateView):
    template_name = 'vozmac/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['motivo_visita'] = (
            RespuestaEncuesta.objects
            .values('p0_tipo_visita')
            .annotate(total=Count('id'))
            .order_by('p0_tipo_visita')
        )
        return context


def sales_metrics(request):
    """Promedios de respuestas Likert (p1..p4) agrupados por MAC.

    Devuelve dos series (una por MAC existente), cada una con 4 valores
    correspondientes a p1..p4. Si hay más de dos MAC, se devuelven todos.
    """
    categories = [
        "Claridad de la información",
        "Amabilidad",
        "Instalaciones",
        "Tiempo de espera",
    ]

    qs = (
        RespuestaEncuesta.objects
        .values("batch__mac")
        .annotate(
            p1=Avg("p1_claridad_info"),
            p2=Avg("p2_amabilidad"),
            p3=Avg("p3_instalaciones"),
            p4=Avg("p4_tiempo_espera"),
        )
        .order_by("batch__mac")
    )

    series = []
    for row in qs:
        mac = row["batch__mac"]
        vals = [row["p1"], row["p2"], row["p3"], row["p4"]]
        # Redondear a 2 decimales y manejar None
        data_vals = [round(v, 2) if v is not None else 0 for v in vals]
        series.append({"name": mac, "data": data_vals})

    return JsonResponse({"categories": categories, "series": series})


def likert_by_mac(request):
    """Promedios de p1..p4 por MAC.

    Respuesta: categories = [MACs...], series = 4 (una por cada pregunta Likert).
    """
    qs = (
        RespuestaEncuesta.objects
        .values("batch__mac")
        .annotate(
            p1=Avg("p1_claridad_info"),
            p2=Avg("p2_amabilidad"),
            p3=Avg("p3_instalaciones"),
            p4=Avg("p4_tiempo_espera"),
        )
        .order_by("batch__mac")
    )

    macs = [row["batch__mac"] for row in qs]

    def safe(v):
        return round(v, 2) if v is not None else 0

    series = [
        {"name": "Claridad de la información", "data": [safe(r["p1"]) for r in qs]},
        {"name": "Amabilidad", "data": [safe(r["p2"]) for r in qs]},
        {"name": "Instalaciones", "data": [safe(r["p3"]) for r in qs]},
        {"name": "Tiempo de espera", "data": [safe(r["p4"]) for r in qs]},
    ]

    return JsonResponse({"categories": macs, "series": series})

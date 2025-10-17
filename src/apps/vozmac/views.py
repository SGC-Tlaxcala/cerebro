import os
import hashlib
import gzip
import logging
import json
from django.views.generic import TemplateView
from django.shortcuts import render
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


def insertar_respuestas(paquete, respuestas):
    """
    Recibe un objeto paquete y un json y lo inserta en RespuestaEncuesta.
    """
    respuestas_para_procesar = []
    try:
        for respuesta_json in respuestas:
            if not respuesta_json:
                continue
            datos = json.loads(respuesta_json)
            datos.pop('device_id', None)
            datos.pop('is_exported', None)
            respuestas_para_procesar.append(RespuestaEncuesta(batch=paquete, **datos))
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
        if form.is_valid():
            archivo = form.cleaned_data['file_name']
            nombre_archivo = archivo.name
            ruta_temporal = os.path.join(settings.MEDIA_ROOT, 'vozmac_temp', nombre_archivo)
            os.makedirs(os.path.dirname(ruta_temporal), exist_ok=True)
            with open(ruta_temporal, 'wb+') as destino:
                for chunk in archivo.chunks():
                    destino.write(chunk)

            try:
                datos_paquete = obtener_datos_paquete(ruta_temporal, nombre_archivo)
                respuestas = datos_paquete.pop('respuestas', None)
                paquete, creado = PaqueteEncuesta.objects.get_or_create(
                    file_name=datos_paquete['file_name'],
                    defaults=datos_paquete
                )
                if not creado:
                    messages.warning(request, 'Este archivo ya fue procesado previamente.')
                else:
                    messages.success(request,
                                     f"Archivo procesado correctamente. {datos_paquete['record_count']} registros detectados.")
                    insertar_respuestas(paquete, respuestas)
            except Exception as e:
                messages.error(request, f'Error al procesar el archivo: {e}')
            finally:
                if os.path.exists(ruta_temporal):
                    os.remove(ruta_temporal)
        else:
            messages.error(request, 'Formulario inválido. Por favor, seleccione un archivo válido.')
        contexto = self.get_context_data(form=form)
        return render(request, self.template_name, contexto)


class VozMACIndex(TemplateView):
    template_name = 'vozmac/index.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

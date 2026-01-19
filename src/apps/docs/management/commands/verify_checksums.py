import os
import time
import pytz
import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

from apps.docs.models import Revision

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Verifica y calcula checksums para las revisiones."

    def handle(self, *args, **options):
        tz = pytz.timezone("America/Mexico_City")
        ahora = timezone.now().astimezone(tz)
        inicio = time.monotonic()

        ok = 0
        calculadas = 0
        faltantes = 0
        inconsistentes = 0

        revisiones = Revision.objects.exclude(archivo__isnull=True).exclude(archivo="")

        if not revisiones.exists():
            self.stdout.write(self.style.WARNING(
                f"[{ahora:%Y-%m-%d %H:%M}] No hay revisiones con archivo para verificar."
            ))
            return

        self.stdout.write(f"[{ahora:%Y-%m-%d %H:%M}] Verificando {revisiones.count()} revisiones...")

        for rev in revisiones:
            if not rev.archivo:
                faltantes += 1
                continue

            try:
                file_path = os.path.join(settings.MEDIA_ROOT, rev.archivo.name)

                if not os.path.exists(file_path):
                    faltantes += 1
                    continue

                checksum_actual = rev.calcular_checksum()

                if not rev.checksum:
                    rev.calcular_y_guardar_checksum()
                    calculadas += 1
                elif rev.checksum == checksum_actual:
                    rev.checksum_verificado_en = timezone.now()
                    rev.save(update_fields=["checksum_verificado_en"])
                    ok += 1
                else:
                    inconsistentes += 1
            except Exception as e:
                logger.exception(f"Error verificando revisión {rev.id}")

        fin = time.monotonic()
        duracion = fin - inicio
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Resumen: OK={ok} | Calculadas={calculadas} | Faltantes={faltantes} | Inconsistentes={inconsistentes}"
        ))
        self.stdout.write(self.style.SUCCESS(
            f"Tiempo total: {duracion:.2f} segundos."
        ))

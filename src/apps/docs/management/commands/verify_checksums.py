import os
import time
import hashlib
import pytz
import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

from apps.docs.models import Revision

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Verifica la integridad de los archivos asociados a revisiones mediante checksum SHA-256."

    def handle(self, *args, **options):
        tz = pytz.timezone("America/Mexico_City")
        ahora = timezone.now().astimezone(tz)
        inicio = time.monotonic()

        revisiones = Revision.objects.exclude(archivo__isnull=True).exclude(archivo="")

        if not revisiones.exists():
            self.stdout.write(self.style.WARNING(
                f"[{ahora:%Y-%m-%d %H:%M}] No hay revisiones con archivo para verificar."
            ))
            return

        ok = 0
        calculadas = 0
        faltantes = 0
        inconsistentes = 0

        self.stdout.write(f"[{ahora:%Y-%m-%d %H:%M}] Verificando {revisiones.count()} revisiones...")

        for rev in revisiones:
            try:
                file_path = os.path.join(settings.MEDIA_ROOT, rev.archivo.name)

                if not os.path.exists(file_path):
                    faltantes += 1
                    self.stdout.write(self.style.ERROR(
                        f"MISSING_FILE  | Revision id={rev.id} | {rev.archivo.name}"
                    ))
                    continue

                # Caso: no hay checksum -> calcular usando save()
                if not rev.checksum:
                    rev.save()
                    calculadas += 1
                    self.stdout.write(self.style.SUCCESS(
                        f"CHECKSUM_CALCULATED | Revision id={rev.id}"
                    ))
                    continue

                # Verificación normal
                sha256 = hashlib.sha256()
                with open(file_path, "rb") as f:
                    for chunk in iter(lambda: f.read(8192), b""):
                        sha256.update(chunk)

                checksum_actual = sha256.hexdigest()

                if checksum_actual == rev.checksum:
                    ok += 1
                else:
                    inconsistentes += 1
                    self.stdout.write(self.style.ERROR(
                        f"MISMATCH | Revision id={rev.id} | esperado={rev.checksum} | actual={checksum_actual}"
                    ))

            except Exception as e:
                logger.exception(f"Error verificando revisión {rev.id}")
                self.stdout.write(self.style.ERROR(
                    f"ERROR | Revision id={rev.id} | {e}"
                ))

        fin = time.monotonic()
        duracion = fin - inicio
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Resumen: OK={ok} | Calculadas={calculadas} | Faltantes={faltantes} | Inconsistentes={inconsistentes}"
        ))
        self.stdout.write(self.style.SUCCESS(
            f"Tiempo total: {duracion:.2f} segundos."
        ))

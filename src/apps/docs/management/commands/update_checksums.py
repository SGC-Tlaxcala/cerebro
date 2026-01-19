from django.core.management.base import BaseCommand
from django.utils.timezone import now
from apps.docs.models import Revision

class Command(BaseCommand):
    help = 'Calcula y actualiza los campos checksum_calculado_en y checksum_verificado_en para todas las revisiones existentes.'

    def handle(self, *args, **kwargs):
        revisiones = Revision.objects.filter(archivo__isnull=False)
        total = revisiones.count()
        actualizadas = 0

        for revision in revisiones:
            if not revision.checksum:
                try:
                    revision.calcular_y_guardar_checksum()
                    revision.checksum_verificado_en = now()
                    revision.save(update_fields=['checksum_verificado_en'])
                    actualizadas += 1
                except FileNotFoundError:
                    self.stdout.write(self.style.WARNING(f"Archivo no encontrado para la revisión ID {revision.id}"))

        self.stdout.write(self.style.SUCCESS(f"Se actualizaron {actualizadas} de {total} revisiones."))

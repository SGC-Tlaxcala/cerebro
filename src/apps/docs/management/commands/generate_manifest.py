import os
import json
from django.conf import settings
from django.core.management.base import BaseCommand
from apps.docs.models import Documento


class Command(BaseCommand):
    help = "Genera el archivo manifest.js en cmi_portatil/ con rutas relativas 'docs/tipo/archivo'"

    def handle(self, *args, **options):
        # Crear el directorio de salida si no existe
        output_dir = os.path.join(settings.MEDIA_ROOT, "cmi_portatil")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        active_docs = Documento.objects.filter(activo=True)
        manifest = {}
        count = 0

        for doc in active_docs:
            rev = doc.latest_revision
            if rev and rev.archivo:
                # Ruta relativa: docs/slug-del-tipo/nombre-del-archivo
                tipo_slug = doc.tipo.slug
                filename = os.path.basename(rev.archivo.name)
                relative_path = f"docs/{tipo_slug}/{filename}"

                manifest[relative_path] = {
                    "hash": rev.checksum or "",
                    "size": rev.archivo.size,
                }
                count += 1

        # Generar contenido JS
        content = f"const SGC_MANIFEST = {json.dumps(manifest, indent=2)};"
        output_path = os.path.join(output_dir, "manifest.js")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        self.stdout.write(
            self.style.SUCCESS(f"Éxito: Se generó {output_path} con {count} archivos.")
        )

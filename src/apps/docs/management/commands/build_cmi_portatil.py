import hashlib
import json
import os
import shutil
import tempfile
import time
from django.core.management.base import BaseCommand

from apps.docs.models import Documento


class Command(BaseCommand):
    help = (
        "Unifica la preparación, generación de manifiesto y validación del CMI Portátil"
    )

    def handle(self, *args, **options):
        start_time = time.time()
        # 1. Crear Staging Area
        build_dir = os.path.join(tempfile.gettempdir(), "cmi_build")
        docs_dir = os.path.join(build_dir, "docs")
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)
        os.makedirs(docs_dir)

        active_docs = Documento.objects.filter(activo=True)
        manifest = {}
        errors = 0

        for doc in active_docs:
            rev = doc.latest_revision
            if not rev or not rev.archivo:
                continue

            # Definir rutas
            tipo_slug = doc.tipo.slug
            filename = os.path.basename(rev.archivo.name)
            rel_path = f"docs/{tipo_slug}/{filename}"
            dest_path = os.path.join(build_dir, rel_path)

            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            # 1.1 Copiar archivo
            shutil.copy2(rev.archivo.path, dest_path)

            # 1.2 Agregar al manifiesto
            manifest[rel_path] = {"hash": rev.checksum or "", "size": rev.archivo.size}

            # 1.3 Verificar copia contra base de datos
            with open(dest_path, "rb") as f:
                sha256 = hashlib.sha256()
                for chunk in iter(lambda: f.read(8192), b""):
                    sha256.update(chunk)
                file_hash = sha256.hexdigest()
                if file_hash != rev.checksum:
                    self.stdout.write(
                        self.style.ERROR(f"Error de integridad: {rel_path}")
                    )
                    errors += 1

        # Generar manifest.js
        with open(os.path.join(build_dir, "manifest.js"), "w", encoding="utf-8") as f:
            f.write(f"const SGC_MANIFEST = {json.dumps(manifest, indent=2)};")

        if errors == 0:
            duration = time.time() - start_time
            self.stdout.write(
                self.style.SUCCESS(
                    f"Staging Area lista en {build_dir} con {len(manifest)} archivos en {duration:.2f} segundos."
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"Proceso completado con {errors} errores de integridad."
                )
            )

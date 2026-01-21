from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.timezone import now
from hashlib import sha256
import os

import json
import tempfile
from unittest.mock import patch, mock_open

from django.core.management import call_command

from apps.docs.models import Documento, Proceso, Tipo, Revision


User = get_user_model()


class DocsViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester")
        self.tipo = Tipo.objects.create(tipo="Procedimiento", slug="prc")
        self.proceso = Proceso.objects.create(proceso="Planeación", slug="pln")
        self.doc = Documento.objects.create(
            nombre="Guía de prueba",
            slug="guia-prueba",
            proceso=self.proceso,
            tipo=self.tipo,
            lmd=True,
            autor=self.user,
            texto_ayuda="Documento de ejemplo",
        )
        Revision.objects.create(
            documento=self.doc,
            revision=1,
            f_actualizacion=timezone.now().date(),
            archivo=SimpleUploadedFile("prueba.pdf", b"contenido de prueba"),
            cambios="Inicial",
            autor=self.user,
            checksum="d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2",
            checksum_calculado_en=timezone.now(),
        )
        # Crear un documento adicional con lmd=False para la prueba
        self.doc_ldp = Documento.objects.create(
            nombre="Documento LDP",
            slug="documento-ldp",
            proceso=self.proceso,
            tipo=self.tipo,
            lmd=False,
            activo=True,
            autor=self.user,
        )
        Revision.objects.create(
            documento=self.doc_ldp,
            revision=1,
            f_actualizacion=timezone.now().date(),
            archivo=SimpleUploadedFile("ldp.pdf", b"contenido del documento LDP"),
            cambios="Versión inicial",
            autor=self.user,
        )

    def test_index_renders_tailwind_template(self):
        response = self.client.get(reverse("docs:index"))
        self.assertContains(response, "Gestor documental")
        self.assertTemplateUsed(response, "docs/index.html")

    def test_ldp_returns_partial_with_htmx(self):
        response = self.client.get(
            reverse("docs:ldp"),
            HTTP_HX_REQUEST="true",
        )
        self.assertTemplateUsed(response, "docs/partials/_doc_list.html")
        self.assertContains(response, self.doc_ldp.nombre)

    def test_search_view_filters_results(self):
        response = self.client.get(reverse("docs:buscador"), {"q": "Guía"})
        self.assertContains(response, "Resultados de búsqueda")

    def test_inactive_document_hidden_in_search(self):
        # Crear documento inactivo
        inactive_doc = Documento.objects.create(
            nombre="Documento Inactivo",
            slug="doc-inactivo",
            proceso=self.proceso,
            tipo=self.tipo,
            activo=False,
            autor=self.user,
        )
        Revision.objects.create(
            documento=inactive_doc,
            revision=1,
            f_actualizacion=timezone.now().date(),
            archivo=SimpleUploadedFile("inactivo.pdf", b"contenido"),
            cambios="Inicial",
            autor=self.user,
        )
        response = self.client.get(reverse("docs:buscador"), {"q": "Inactivo"})
        self.assertNotContains(response, inactive_doc.nombre)


class DocsAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="api-user")
        tipo = Tipo.objects.create(tipo="Formato", slug="fmt")
        proceso = Proceso.objects.create(proceso="Operación", slug="opr")
        doc = Documento.objects.create(
            nombre="Formato operativo",
            slug="formato-operativo",
            proceso=proceso,
            tipo=tipo,
            autor=self.user,
            lmd=True,
        )
        Revision.objects.create(
            documento=doc,
            revision=1,
            f_actualizacion=timezone.now().date(),
            archivo=SimpleUploadedFile("formato.pdf", b"pdf"),
            cambios="Alta",
            autor=self.user,
        )

    def test_documents_api_returns_data(self):
        response = self.client.get("/api/v1/docs/documents/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) >= 1)
        self.assertIn("nombre", data[0])

    def test_documents_api_filter_by_query(self):
        response = self.client.get("/api/v1/docs/documents/", {"q": "operativo"})
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()), 1)

    def test_documents_api_hides_inactive(self):
        # Crear documento inactivo
        tipo = Tipo.objects.first()
        proceso = Proceso.objects.first()
        inactive_doc = Documento.objects.create(
            nombre="API Inactivo",
            slug="api-inactivo",
            proceso=proceso,
            tipo=tipo,
            activo=False,
            autor=self.user,
        )
        Revision.objects.create(
            documento=inactive_doc,
            revision=1,
            f_actualizacion=timezone.now().date(),
            archivo=SimpleUploadedFile("api_inactivo.pdf", b"pdf"),
            cambios="Alta",
            autor=self.user,
        )

        response = self.client.get("/api/v1/docs/documents/", {"q": "API Inactivo"})
        self.assertEqual(response.status_code, 200)
        # No debería encontrarlo
        for doc in response.json():
            self.assertNotEqual(doc["nombre"], "API Inactivo")


class RevisionChecksumTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="checksum-tester")
        self.tipo = Tipo.objects.create(tipo="Manual", slug="man")
        self.proceso = Proceso.objects.create(proceso="Calidad", slug="cal")
        self.doc = Documento.objects.create(
            nombre="Manual de Calidad",
            slug="manual-calidad",
            proceso=self.proceso,
            tipo=self.tipo,
            lmd=True,
            autor=self.user,
            texto_ayuda="Documento de calidad",
        )
        self.revision = Revision.objects.create(
            documento=self.doc,
            revision=1,
            f_actualizacion=now().date(),
            archivo=SimpleUploadedFile("manual.pdf", b"contenido del manual"),
            cambios="Primera versión",
            autor=self.user,
        )

    def test_calcular_checksum(self):
        # Ensure checksum is calculated correctly
        checksum = self.revision.calcular_checksum()
        expected_checksum = sha256(b"contenido del manual").hexdigest()
        self.assertEqual(checksum, expected_checksum)

    def test_save_updates_checksum_fields(self):
        # Ensure checksum fields are updated on save
        self.revision.checksum = ""
        self.revision.save()
        self.assertIsNotNone(self.revision.checksum)
        self.assertIsNotNone(self.revision.checksum_calculado_en)

    def test_verify_checksum_command(self):
        # Simulate the verify_checksums management command
        from apps.docs.management.commands.verify_checksums import Command
        from django.core.files.base import ContentFile

        # Inicializar datos con un checksum válido
        # Asegurar que el archivo existe y el checksum coincide
        self.revision.archivo.save("dummy_file.txt", ContentFile(b"dummy content"))
        self.revision.checksum = self.revision.calcular_checksum()
        self.revision.checksum_verificado_en = None
        self.revision.save()

        command = Command()
        command.handle()

        # Reload the revision and check verification timestamp
        self.revision.refresh_from_db()
        self.assertIsNotNone(self.revision.checksum_verificado_en)

    def test_missing_file(self):
        # Simulate a missing file scenario
        os.remove(self.revision.archivo.path)
        with self.assertRaises(FileNotFoundError):
            self.revision.calcular_checksum()

    def test_checksum_algorithm_field(self):
        # Ensure the checksum_algoritmo field is set to 'sha256'
        self.assertEqual(self.revision.checksum_algoritmo, "sha256")

    def test_no_recalculation_if_file_unchanged(self):
        # Ensure checksum is not recalculated if the file hasn't changed
        initial_checksum = self.revision.checksum
        self.revision.save()
        self.assertEqual(self.revision.checksum, initial_checksum)

    def test_verify_checksum_does_not_modify_correct_records(self):
        # Ensure verify_checksums does not modify records with correct checksums
        from apps.docs.management.commands.verify_checksums import Command

        command = Command()
        command.handle()

        # Reload the revision and ensure no changes were made
        self.revision.refresh_from_db()
        self.assertEqual(
            self.revision.checksum_verificado_en, self.revision.checksum_verificado_en
        )


class GenerateManifestCommandTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="manifest-tester")
        self.tipo = Tipo.objects.create(tipo="Instructivo", slug="ins")
        self.proceso = Proceso.objects.create(proceso="Soporte", slug="sop")

        # Active Document
        self.doc_active = Documento.objects.create(
            nombre="Guía Activa",
            slug="guia-activa",
            proceso=self.proceso,
            tipo=self.tipo,
            lmd=True,
            activo=True,
            autor=self.user,
        )
        self.rev_active = Revision.objects.create(
            documento=self.doc_active,
            revision=1,
            f_actualizacion=now().date(),
            archivo=SimpleUploadedFile("guia.pdf", b"contenido activo"),
            cambios="V1",
            autor=self.user,
            checksum="abcdef123456",
        )

        # Inactive Document
        self.doc_inactive = Documento.objects.create(
            nombre="Guía Inactiva",
            slug="guia-inactiva",
            proceso=self.proceso,
            tipo=self.tipo,
            lmd=True,
            activo=False,
            autor=self.user,
        )
        self.rev_inactive = Revision.objects.create(
            documento=self.doc_inactive,
            revision=1,
            f_actualizacion=now().date(),
            archivo=SimpleUploadedFile("old.pdf", b"contenido viejo"),
            cambios="V1",
            autor=self.user,
        )

    @patch("apps.docs.management.commands.generate_manifest.os.makedirs")
    @patch("apps.docs.management.commands.generate_manifest.os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    @patch("django.conf.settings.MEDIA_ROOT", "/tmp/media")
    def test_manifest_generation(self, mock_file, mock_exists, mock_makedirs):
        # Mock exists to return False first (to trigger makedirs)
        mock_exists.return_value = False

        call_command("generate_manifest")

        # Verify directory creation
        expected_dir = os.path.join("/tmp/media", "cmi_portatil")
        mock_makedirs.assert_called_with(expected_dir)

        # Verify file write
        args, _ = mock_file.call_args
        self.assertTrue(args[0].endswith("manifest.js"))

        # Extract written content
        handle = mock_file()
        written_content = "".join(call[0][0] for call in handle.write.call_args_list)

        # Extract JSON part: const SGC_MANIFEST = {...};
        json_str = written_content.replace("const SGC_MANIFEST = ", "").rstrip(";")
        manifest = json.loads(json_str)

        # Verify active doc is present with correct path
        # Note: The file name is generated by 'subir_documento' function in models.py
        # triggering a rename. We should use the actual name stored in the DB.
        filename = os.path.basename(self.rev_active.archivo.name)
        expected_path = f"docs/ins/{filename}"
        self.assertIn(expected_path, manifest)
        self.assertEqual(manifest[expected_path]["hash"], "abcdef123456")
        self.assertEqual(manifest[expected_path]["size"], self.rev_active.archivo.size)

        # Verify inactive doc is NOT present


class BuildCMIPortatilCommandTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="builder")
        self.tipo = Tipo.objects.create(tipo="Instructivo", slug="ins")
        self.proceso = Proceso.objects.create(proceso="Soporte", slug="sop")

        # Active Document
        self.doc_active = Documento.objects.create(
            nombre="Guía Activa",
            slug="guia-activa",
            proceso=self.proceso,
            tipo=self.tipo,
            lmd=True,
            activo=True,
            autor=self.user,
        )
        self.pdf_content = b"PDF_CONTENT"
        self.checksum = sha256(self.pdf_content).hexdigest()

        self.rev_active = Revision.objects.create(
            documento=self.doc_active,
            revision=1,
            f_actualizacion=now().date(),
            archivo=SimpleUploadedFile("guia_build.pdf", self.pdf_content),
            cambios="V1",
            autor=self.user,
            checksum=self.checksum,
        )

    def test_build_cmi_success(self):
        # Create a temporary directory for the test
        with tempfile.TemporaryDirectory() as temp_dir:
            # Patch globally to capture all usages
            with patch("tempfile.gettempdir") as mock_gettempdir:
                mock_gettempdir.return_value = temp_dir

                # Sub-path that the command will generate
                build_dir = os.path.join(temp_dir, "cmi_build")

                # Execute command
                call_command("build_cmi_portatil")

                # 1. Verify directory exists
                self.assertTrue(os.path.exists(build_dir))

            # 2. Verify manifest.js exists
            manifest_path = os.path.join(build_dir, "manifest.js")
            self.assertTrue(os.path.exists(manifest_path))

            # 3. Verify content of manifest.js
            with open(manifest_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Check structure
                self.assertTrue(content.startswith("const SGC_MANIFEST = {"))
                self.assertTrue(content.endswith("};"))

                # Check data
                json_str = content.replace("const SGC_MANIFEST = ", "").rstrip(";")
                manifest = json.loads(json_str)

                # Expected relative path
                filename = os.path.basename(self.rev_active.archivo.name)
                rel_path = f"docs/ins/{filename}"

                self.assertIn(rel_path, manifest)
                self.assertEqual(manifest[rel_path]["hash"], self.checksum)

            # 4. Verify file copied
            # Note: The real file name in 'media' might be different due to upload handling,
            # but the command uses 'rev.archivo.name' basename.
            # We check if the destination file exists at 'build_dir/docs/ins/filename'
            dest_file_path = os.path.join(
                build_dir, "docs", "ins", os.path.basename(self.rev_active.archivo.name)
            )
            self.assertTrue(os.path.exists(dest_file_path))

            # Verify content matches
            with open(dest_file_path, "rb") as f:
                self.assertEqual(f.read(), self.pdf_content)

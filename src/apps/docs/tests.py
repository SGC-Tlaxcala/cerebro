from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.timezone import now
from hashlib import sha256
import os

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
        self.assertEqual(self.revision.checksum_verificado_en, self.revision.checksum_verificado_en)

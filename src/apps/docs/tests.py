from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.utils import timezone

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
        self.assertContains(response, self.doc.nombre)

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

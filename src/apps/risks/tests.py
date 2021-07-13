from django.test import TestCase
from django.test import Client


class RisksTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/risks/')

    def test_create(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, '<title>Gestión de Riesgos</title>')
        self.assertContains(self.response, 'bootstrap.min.css')
        self.assertContains(self.response, 'jumbotron')
        self.assertContains(self.response, 'fa-bug')
        self.assertContains(self.response, "Agregar riesgo")

    def test_evaluate_risk(self):
        self.assertContains(self.response, "Evaluar riesgo")

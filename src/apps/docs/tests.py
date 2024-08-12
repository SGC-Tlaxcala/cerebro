"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

# Write test for models in models.py
from .models import Tipo, Proceso, Documento

class TipoModelTest(TestCase):
    def setUp(self):
        Tipo.objects.create(tipo='Planos', slug='pln')

    def test_tipo_model(self):
        tipo = Tipo.objects.get(tipo='Planos')
        self.assertEqual(tipo.slug, 'pln')

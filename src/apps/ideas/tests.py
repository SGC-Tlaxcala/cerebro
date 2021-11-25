from django.test import TestCase
from django.urls import reverse
from django.urls import resolve

from apps.ideas.views import IdeasList


# Create your tests here.
class TestUrls(TestCase):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_resolution_for_ideas(self):
        resolver = resolve('/mejora/ideas')
        self.assertEqual(resolver.view_name, 'ideas:ideas')

from django.apps import AppConfig
from watson import search as watson


class DocsConfig(AppConfig):
    name = 'apps.docs'
    verbose_name = 'Documentación del Sistema'

    def ready(self):
        documento = self.get_model("Documento")
        watson.register(documento, field=('texto_ayuda', 'nombre', 'slug'))

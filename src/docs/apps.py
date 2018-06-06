from django.apps import AppConfig
from watson import search as watson


class DocsConfig(AppConfig):
    name = 'docs'
    verbose_name = 'Documentación del Sistema'

    def ready(self):
        Documento = self.get_model("Documento")
        watson.register(Documento, field=('texto_ayuda', 'nombre', 'slug'))

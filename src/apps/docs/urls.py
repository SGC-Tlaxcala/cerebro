from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProcesoViewSet, TipoViewSet, DocumentoViewSet, RevisionViewSet, ReporteViewSet
)

app_name = 'docs'

router = DefaultRouter()
router.register(r'procesos', ProcesoViewSet)
router.register(r'tipos', TipoViewSet)
router.register(r'documentos', DocumentoViewSet)
router.register(r'revisiones', RevisionViewSet)
router.register(r'reportes', ReporteViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]

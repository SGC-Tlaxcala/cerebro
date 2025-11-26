from rest_framework.routers import DefaultRouter

from .views import DocumentViewSet, ProcesoViewSet, TipoViewSet

router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='documents')
router.register(r'tipos', TipoViewSet, basename='document-types')
router.register(r'procesos', ProcesoViewSet, basename='document-processes')

urlpatterns = router.urls

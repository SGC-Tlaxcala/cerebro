from rest_framework.routers import DefaultRouter

from .views import PlanViewSet, AccionViewSet, SeguimientoViewSet


router = DefaultRouter()
router.register(r"plans", PlanViewSet, basename="pas-plan")
router.register(r"actions", AccionViewSet, basename="pas-accion")
router.register(r"followups", SeguimientoViewSet, basename="pas-seguimiento")

urlpatterns = router.urls

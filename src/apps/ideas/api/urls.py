from rest_framework.routers import DefaultRouter

from .views import IdeaViewSet


router = DefaultRouter()
router.register(r'', IdeaViewSet, basename='ideas')

urlpatterns = router.urls

from django.urls import path
from .views import MotivoAPIView, SatisfaccionAPIView

urlpatterns = [
    path('motivo', MotivoAPIView.as_view(), name='api_motivo'),
    path('satisfaccion', SatisfaccionAPIView.as_view(), name='api_satisfaccion'),
]

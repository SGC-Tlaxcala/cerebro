from django.urls import path
from .views import MotivoAPIView, SatisfaccionAPIView, MacsAPIView, SeguimientoAPIView

urlpatterns = [
    path('motivo', MotivoAPIView.as_view(), name='api_motivo'),
    path('satisfaccion', SatisfaccionAPIView.as_view(), name='api_satisfaccion'),
    path('macs', MacsAPIView.as_view(), name='api_macs'),
    path('seguimiento', SeguimientoAPIView.as_view(), name='api_seguimiento'),
]

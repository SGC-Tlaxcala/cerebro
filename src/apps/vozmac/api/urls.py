from django.urls import path
from .views import MotivoAPIView

urlpatterns = [
    path('motivo', MotivoAPIView.as_view(), name='api_motivo'),
]


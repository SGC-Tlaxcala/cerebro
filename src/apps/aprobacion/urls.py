from django.urls import path
from apps.aprobacion.views import Portada


app_name = 'aprobacion'
urlpatterns = [
    path('', Portada.as_view(), name='index')
]

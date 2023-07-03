from django.urls import path
from .views import ProductosCartograficos

app_name = 'carto'
urlpatterns = [
    path('', ProductosCartograficos.as_view(), name='index'),
]

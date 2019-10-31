from django.urls import path
from apps.mc.views import Index


app_name = 'mc'
urlpatterns = [
    path('', Index.as_view(), name='index')
]

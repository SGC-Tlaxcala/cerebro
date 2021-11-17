from django.urls import path
from apps.ideas.views import IdeasIndex

app_name = 'ideas'
urlpatterns = [
    path('', IdeasIndex.as_view(), name='index')
]

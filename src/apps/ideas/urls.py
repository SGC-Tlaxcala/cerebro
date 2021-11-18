from django.urls import path
from apps.ideas.views import IdeasIndex, IdeasList

app_name = 'ideas'
urlpatterns = [
    path('', IdeasIndex.as_view(), name='index'),
    path('ideas', IdeasList.as_view(), name='ideas')
]

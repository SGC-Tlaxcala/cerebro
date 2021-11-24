from django.urls import path
from apps.ideas.views import IdeasIndex, IdeaDetail

app_name = 'ideas'
urlpatterns = [
    path('', IdeasIndex.as_view(), name='index'),
    path('detalle/<int:pk>/', IdeaDetail.as_view(), name='detalle')
]

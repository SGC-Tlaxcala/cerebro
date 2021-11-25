from django.urls import path
from .views import IdeasIndex, IdeaDetail, IdeaAdd

app_name = 'ideas'
urlpatterns = [
    path('', IdeasIndex.as_view(), name='index'),
    path('add/', IdeaAdd.as_view(), name='add'),
    path('detalle/<int:pk>/', IdeaDetail.as_view(), name='detalle')
]

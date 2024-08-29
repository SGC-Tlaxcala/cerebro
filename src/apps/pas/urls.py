from django.urls import path
from .views import (
    PASIndex, PASAdd
)


app_name = 'pas'
urlpatterns = [
    path('', PASIndex.as_view(), name='index'),
    path('add/', PASAdd.as_view(), name='add'),

    # path('detalle/<int:pk>/', IdeaDetail.as_view(), name='detalle')
]

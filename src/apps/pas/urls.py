from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    PASIndex, PASAdd
)


app_name = 'pas'
urlpatterns = [
    path('', login_required(PASIndex.as_view()), name='index'),
    path('add/', PASAdd.as_view(), name='add'),

    # path('detalle/<int:pk>/', IdeaDetail.as_view(), name='detalle')
]

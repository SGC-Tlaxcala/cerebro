from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    PASIndex, PASAdd, PASDetail, PASAction
)


app_name = 'pas'
urlpatterns = [
    path('', login_required(PASIndex.as_view()), name='index'),
    path('add/', login_required(PASAdd.as_view()), name='add'),
    path('detalle/<int:pk>/', login_required(PASDetail.as_view()), name='detalle'),
    path('accion/<int:pk>/', login_required(PASAction.as_view()), name='action')
]

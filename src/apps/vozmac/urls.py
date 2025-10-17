from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
    VozMACAdd,
    VozMACIndex,
)

app_name = 'vozmac'
urlpatterns = [
    path('', VozMACIndex.as_view(), name='index'),
    path('add/', login_required(VozMACAdd.as_view()), name='add'),
]

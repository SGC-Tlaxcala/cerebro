# coding: utf-8
# app: productividad
# module: urls
# date: 26 Aug 2018
# author: Javier Sanchez Toledano <js.toledano@me.com>
"""Patrones de URI para productividad"""

from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from apps.productividad.views import CifrasUpload

app_name = 'cifras'
urlpatterns = [
    path('', login_required(CifrasUpload.as_view()), name="index")
]

# coding: utf-8
# app: cecyrd
# module: urls
# date: 26 Aug 2018
# author: Javier Sanchez Toledano <js.toledano@me.com>
"""Patrones de URI para productividad"""

from django.urls import path
from apps.cecyrd.views import CecyrdIndex

app_name = 'cecyrd'
urlpatterns = [
    path('', CecyrdIndex.as_view(), name='index')
]

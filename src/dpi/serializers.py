# coding: utf-8
#         app: dpi
#      module: serializers
#        date: miércoles, 30 de mayo de 2018 - 08:55
# description: Serializadores para expedientes DPI y USI
# pylint: disable=W0613,R0201,R0903

from rest_framework import serializers
from dpi.models import ExpedienteDPI


class ExpedienteSerializer(serializers.Serializer):
    tipo = serializers.CharField(max_length=3)
    folio = serializers.CharField(max_length=13)
    nombre = serializers.CharField(max_length=100)
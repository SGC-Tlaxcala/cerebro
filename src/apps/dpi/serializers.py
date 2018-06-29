# coding: utf-8
#         app: dpi
#      module: serializers
#        date: miércoles, 30 de mayo de 2018 - 08:55
# description: Serializadores para expedientes DPI y USI
# pylint: disable=W0613,R0201,R0903

from rest_framework import serializers
from apps.dpi.models import ExpedienteDPI


class ExpedienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpedienteDPI
        fields = ['tipo', 'folio', 'nombre']
        editable = False

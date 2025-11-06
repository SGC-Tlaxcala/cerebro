from rest_framework import serializers

from apps.pas.models import Plan, Accion, Seguimiento


class PlanSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Plan
        fields = "__all__"


class AccionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Accion
        fields = "__all__"


class SeguimientoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Seguimiento
        fields = "__all__"

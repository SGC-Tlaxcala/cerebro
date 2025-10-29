from rest_framework import permissions, viewsets
from rest_framework.exceptions import ValidationError

from apps.kpi.models import Campaign
from .serializers import CampaignSerializer


class CampaignViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provee información consolidada de las campañas KPI (CAP/CAI),
    incluyendo detalle mensual y métricas derivadas para tableros.
    """

    serializer_class = CampaignSerializer
    queryset = Campaign.objects.none()
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        queryset = (
            Campaign.objects.all()
            .prefetch_related('tramitemensual_set')
            .order_by('-year', 'campaign_type')
        )

        year_param = self.request.query_params.get('year')
        if year_param:
            try:
                year = int(year_param)
            except (TypeError, ValueError):
                raise ValidationError({'year': 'El año debe ser un número entero.'})
            queryset = queryset.filter(year=year)

        type_param = self.request.query_params.get('type')
        if type_param:
            type_param = type_param.upper()
            valid_types = {choice[0] for choice in Campaign.TYPE_CHOICES}
            if type_param not in valid_types:
                valid = ', '.join(sorted(valid_types))
                raise ValidationError({'type': f"Tipo inválido. Valores permitidos: {valid}."})
            queryset = queryset.filter(campaign_type=type_param)

        return queryset

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from apps.vozmac.models import RespuestaEncuesta

class MotivoAPIView(APIView):
    """
    API de solo lectura para motivo de visita.
    Devuelve una lista de dicts: [{"p0_tipo_visita": int, "total": int}, ...]
    Permite filtrar por distrito con el parámetro 'd'.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        distrito = request.GET.get('d')
        queryset = RespuestaEncuesta.objects.all()
        if distrito and distrito != '0':
            queryset = queryset.filter(distrito=distrito)
        data = (
            queryset
            .values('p0_tipo_visita')
            .annotate(total=Count('id'))
            .order_by('p0_tipo_visita')
        )
        return Response(list(data), status=status.HTTP_200_OK)


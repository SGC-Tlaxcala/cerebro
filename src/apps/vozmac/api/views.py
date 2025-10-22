from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Avg
from django.utils import timezone
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


class SatisfaccionAPIView(APIView):
    """
    API de solo lectura para métricas de satisfacción (preguntas p1..p4) para el año en curso.
    Devuelve para cada pregunta:
      - average: promedio de respuestas (float)
      - total: número de respuestas consideradas
      - distribution: dict con conteo por valor 1..5
      - favorable_count: conteo de respuestas 4 y 5
      - unfavorable_count: conteo de respuestas 1,2,3
      - favorable_pct: porcentaje favorable (0-100)

    Acepta parámetro opcional 'd' para filtrar por `distrito`.
    """
    authentication_classes = []
    permission_classes = []

    QUESTIONS = [
        ('p1_claridad_info', 'Claridad de la información'),
        ('p2_amabilidad', 'Amabilidad'),
        ('p3_instalaciones', 'Instalaciones'),
        ('p4_tiempo_espera', 'Tiempo de espera'),
    ]

    def get(self, request, format=None):
        distrito = request.GET.get('d')
        now = timezone.now()
        year = now.year
        qs = RespuestaEncuesta.objects.filter(created_at__year=year)
        if distrito and distrito != '0':
            qs = qs.filter(distrito=distrito)

        result = {}
        total_responses = qs.count()

        for field, label in self.QUESTIONS:
            # distribution values 1..5
            dist_qs = qs.values(field).annotate(total=Count('id'))
            dist_map = {str(item[field]): item['total'] for item in dist_qs}
            distribution = {str(v): dist_map.get(str(v), 0) for v in range(1, 6)}

            # averages
            avg_obj = qs.aggregate(avg=Avg(field))
            avg = avg_obj.get('avg') or 0

            favorable = distribution.get('4', 0) + distribution.get('5', 0)
            unfavorable = distribution.get('1', 0) + distribution.get('2', 0) + distribution.get('3', 0)
            favorable_pct = (favorable / (favorable + unfavorable) * 100) if (favorable + unfavorable) > 0 else 0

            result[field] = {
                'label': label,
                'average': round(float(avg), 2),
                'total': sum(distribution.values()),
                'distribution': distribution,
                'favorable_count': favorable,
                'unfavorable_count': unfavorable,
                'favorable_pct': round(float(favorable_pct), 2),
            }

        response = {
            'year': year,
            'distrito': int(distrito) if distrito and distrito != '0' else None,
            'total_responses': total_responses,
            'by_question': result,
        }

        return Response(response, status=status.HTTP_200_OK)

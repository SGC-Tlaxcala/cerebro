from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Avg
from django.utils import timezone
from django.db.models.functions import TruncMonth
from apps.vozmac.models import RespuestaEncuesta
from datetime import datetime

class MotivoAPIView(APIView):
    """
    API de solo lectura para motivo de visita.
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
            dist_qs = qs.values(field).annotate(total=Count('id'))
            dist_map = {str(item[field]): item['total'] for item in dist_qs}
            distribution = {str(v): dist_map.get(str(v), 0) for v in range(1, 6)}

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

class MacsAPIView(APIView):
    """
    API de solo lectura para obtener los MACs únicos.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        distrito_param = request.GET.get('d')
        queryset = RespuestaEncuesta.objects.all()

        if distrito_param and distrito_param != '0':
            try:
                distrito_int = int(distrito_param)
                queryset = queryset.filter(distrito=distrito_int)
            except ValueError:
                return Response({"error": "Invalid district parameter. Must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        macs = queryset.values_list('mac', flat=True).distinct()

        return Response(list(macs), status=status.HTTP_200_OK)


class SeguimientoAPIView(APIView):
    """
    API de solo lectura para el seguimiento mensual de promedios.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        distrito_param = request.GET.get('d')
        today = datetime.now()
        previous_year = today.year - 1

        queryset = RespuestaEncuesta.objects.filter(created_at__year=previous_year)

        if distrito_param and distrito_param != '0':
            try:
                distrito_int = int(distrito_param)
                queryset = queryset.filter(distrito=distrito_int)
            except ValueError:
                return Response({"error": "Invalid district parameter."}, status=status.HTTP_400_BAD_REQUEST)

        question_fields = {
            'p1_claridad_info': 'Claridad de la información',
            'p2_amabilidad': 'Amabilidad',
            'p3_instalaciones': 'Instalaciones',
            'p4_tiempo_espera': 'Tiempo de espera',
        }

        monthly_averages = queryset.annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(
            avg_p1=Avg('p1_claridad_info'),
            avg_p2=Avg('p2_amabilidad'),
            avg_p3=Avg('p3_instalaciones'),
            avg_p4=Avg('p4_tiempo_espera'),
        ).order_by('month')

        month_data_map = {entry['month'].month: entry for entry in monthly_averages}

        labels = [datetime(previous_year, i, 1).strftime('%b') for i in range(1, 13)]

        def get_monthly_data(avg_key):
            data = []
            for i in range(1, 13):
                avg_val = month_data_map.get(i, {}).get(avg_key)
                data.append(round(avg_val, 2) if avg_val is not None else 0)
            return data

        chart_data = {
            'labels': labels,
            'datasets': [
                {'label': question_fields['p1_claridad_info'], 'data': get_monthly_data('avg_p1'), 'borderColor': 'rgba(255, 99, 132, 1)'},
                {'label': question_fields['p2_amabilidad'], 'data': get_monthly_data('avg_p2'), 'borderColor': 'rgba(54, 162, 235, 1)'},
                {'label': question_fields['p3_instalaciones'], 'data': get_monthly_data('avg_p3'), 'borderColor': 'rgba(255, 206, 86, 1)'},
                {'label': question_fields['p4_tiempo_espera'], 'data': get_monthly_data('avg_p4'), 'borderColor': 'rgba(75, 192, 192, 1)'},
            ]
        }

        return Response(chart_data, status=status.HTTP_200_OK)

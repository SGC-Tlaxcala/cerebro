import csv
from datetime import datetime

from django.db.models import Count, Avg
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.vozmac.models import RespuestaEncuesta

class MotivoAPIView(APIView):
    """
    API de solo lectura para motivo de visita.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        distrito = request.GET.get('d')
        mac_param = (request.GET.get('mac') or '').strip()
        mac_filter = mac_param or None

        queryset = RespuestaEncuesta.objects.all()
        if mac_filter:
            queryset = queryset.filter(mac=mac_filter)
        elif distrito and distrito != '0':
            try:
                distrito_int = int(distrito)
            except ValueError:
                return Response({"error": "Invalid district parameter."}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(distrito=distrito_int)
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
        mac_param = (request.GET.get('mac') or '').strip()
        mac_filter = mac_param or None
        now = timezone.now()
        year = now.year
        qs = RespuestaEncuesta.objects.filter(created_at__year=year)
        selected_distrito = None

        if mac_filter:
            qs = qs.filter(mac=mac_filter)
        elif distrito and distrito != '0':
            try:
                selected_distrito = int(distrito)
                qs = qs.filter(distrito=selected_distrito)
            except ValueError:
                return Response({"error": "Invalid district parameter."}, status=status.HTTP_400_BAD_REQUEST)

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
            'distrito': selected_distrito,
            'mac': mac_filter,
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

        macs = (
            queryset
            .order_by('mac')
            .values_list('mac', flat=True)
            .distinct()
        )

        return Response(list(macs), status=status.HTTP_200_OK)


class ExportEncuestasCSVAPIView(APIView):
    """
    Exporta las encuestas filtradas a un archivo CSV.
    """
    authentication_classes = []
    permission_classes = []

    HEADERS = [
        'fecha',
        'entidad',
        'distrito',
        'mac',
        'p0_tipo_visita',
        'p1_claridad_info',
        'p2_amabilidad',
        'p3_instalaciones',
        'p4_tiempo_espera',
    ]

    def get(self, request, format=None):
        distrito = request.GET.get('d')
        mac_param = (request.GET.get('mac') or '').strip()
        mac_filter = mac_param or None

        queryset = RespuestaEncuesta.objects.select_related('batch').all()

        if mac_filter:
            queryset = queryset.filter(mac=mac_filter)
        elif distrito and distrito != '0':
            try:
                distrito_int = int(distrito)
                queryset = queryset.filter(distrito=distrito_int)
            except ValueError:
                return Response({"error": "Invalid district parameter."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = queryset.order_by('-created_at')

        timestamp = timezone.localtime(timezone.now()).strftime('%Y%m%d_%H%M%S')
        filename = f'vozmac_encuestas_{timestamp}.csv'

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        response.write('\ufeff')  # UTF-8 BOM for Excel compatibility
        writer = csv.writer(response)
        writer.writerow(self.HEADERS)

        motivo_labels = {
            1: 'Trámite',
            2: 'Credencial',
        }

        for encuesta in queryset.iterator():
            created_at = timezone.localtime(encuesta.created_at).strftime('%Y-%m-%d %H:%M:%S')
            motivo = motivo_labels.get(encuesta.p0_tipo_visita, encuesta.p0_tipo_visita)
            writer.writerow([
                created_at,
                encuesta.entidad,
                encuesta.distrito,
                encuesta.mac,
                motivo,
                encuesta.p1_claridad_info,
                encuesta.p2_amabilidad,
                encuesta.p3_instalaciones,
                encuesta.p4_tiempo_espera,
            ])

        return response


class SeguimientoAPIView(APIView):
    """
    API de solo lectura para el seguimiento mensual de promedios.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        distrito_param = request.GET.get('d')
        mac_param = (request.GET.get('mac') or '').strip()
        mac_filter = mac_param or None
        today = timezone.now()
        distrito = None

        base_queryset = RespuestaEncuesta.objects.all()

        if mac_filter:
            base_queryset = base_queryset.filter(mac=mac_filter)
        elif distrito_param and distrito_param != '0':
            try:
                distrito = int(distrito_param)
            except ValueError:
                return Response({"error": "Invalid district parameter."}, status=status.HTTP_400_BAD_REQUEST)
            base_queryset = base_queryset.filter(distrito=distrito)

        years_to_try = [today.year, today.year - 1]
        selected_year = None
        queryset = None

        for year in years_to_try:
            candidate_queryset = base_queryset.filter(created_at__year=year)
            if candidate_queryset.exists():
                selected_year = year
                queryset = candidate_queryset
                break

        if queryset is None:
            selected_year = years_to_try[0]
            queryset = base_queryset.filter(created_at__year=selected_year)

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

        month_data_map = {
            entry['month'].month: entry
            for entry in monthly_averages
            if entry.get('month') is not None
        }

        spanish_months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        labels = [spanish_months[i - 1] for i in range(1, 13)]

        def get_monthly_data(avg_key):
            data = []
            for i in range(1, 13):
                avg_val = month_data_map.get(i, {}).get(avg_key)
                if avg_val is None:
                    data.append(0.0)
                else:
                    data.append(round(float(avg_val), 2))
            return data

        chart_data = {
            'year': selected_year,
            'distrito': distrito,
            'mac': mac_filter,
            'total_responses': queryset.count(),
            'labels': labels,
            'datasets': [
                {'label': question_fields['p1_claridad_info'], 'data': get_monthly_data('avg_p1'), 'borderColor': 'rgba(255, 99, 132, 1)'},
                {'label': question_fields['p2_amabilidad'], 'data': get_monthly_data('avg_p2'), 'borderColor': 'rgba(54, 162, 235, 1)'},
                {'label': question_fields['p3_instalaciones'], 'data': get_monthly_data('avg_p3'), 'borderColor': 'rgba(255, 206, 86, 1)'},
                {'label': question_fields['p4_tiempo_espera'], 'data': get_monthly_data('avg_p4'), 'borderColor': 'rgba(75, 192, 192, 1)'},
            ]
        }

        return Response(chart_data, status=status.HTTP_200_OK)

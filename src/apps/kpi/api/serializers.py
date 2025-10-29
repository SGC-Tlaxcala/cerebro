from decimal import Decimal
from typing import List

from rest_framework import serializers

from apps.kpi.models import Campaign, TramiteMensual


class CampaignSerializer(serializers.ModelSerializer):
    """
    Serializador que expone la información relevante de una campaña KPI,
    incluyendo métricas resumidas y el detalle mensual necesario para
    alimentar tableros de control.
    """

    campaign_type_display = serializers.CharField(
        source='get_campaign_type_display',
        read_only=True,
    )
    goal = serializers.SerializerMethodField()
    monthly_data = serializers.SerializerMethodField()
    metrics = serializers.SerializerMethodField()
    charts = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = (
            'id',
            'year',
            'campaign_type',
            'campaign_type_display',
            'goal',
            'forecast',
            'acumulado',
            'avance',
            'monthly_data',
            'metrics',
            'charts',
        )

    @staticmethod
    def _as_float(value) -> float:
        if value is None:
            return 0.0
        if isinstance(value, Decimal):
            return float(value)
        return float(value)

    @staticmethod
    def _month_label(month: int) -> str:
        labels = [
            'Enero', 'Febrero', 'Marzo', 'Abril',
            'Mayo', 'Junio', 'Julio', 'Agosto',
            'Septiembre', 'Octubre', 'Noviembre', 'Diciembre',
        ]
        if 1 <= month <= 12:
            return labels[month - 1]
        return str(month)

    def get_goal(self, obj: Campaign) -> float:
        return self._as_float(obj.goal)

    def _sorted_tramites(self, obj: Campaign) -> List[TramiteMensual]:
        if not hasattr(obj, '_prefetched_tramites'):
            obj._prefetched_tramites = sorted(
                obj.tramitemensual_set.all(), key=lambda item: item.month
            )
        return obj._prefetched_tramites

    def get_monthly_data(self, obj: Campaign):
        mensualidades = self._sorted_tramites(obj)
        forecast = obj.forecast or 0
        goal_pct = self._as_float(obj.goal)
        goal_target = (goal_pct / 100.0 * forecast) if goal_pct else None

        acumulado = 0
        monthly_rows = []

        for tramite in mensualidades:
            acumulado += tramite.tramites
            avance_pct = (acumulado / forecast * 100.0) if forecast else 0.0
            avance_goal = (
                (acumulado / goal_target * 100.0) if goal_target else None
            )
            monthly_rows.append(
                {
                    'month': tramite.month,
                    'label': self._month_label(tramite.month),
                    'tramites': tramite.tramites,
                    'acumulado': acumulado,
                    'avance_pct': round(avance_pct, 2),
                    'avance_vs_goal_pct': round(avance_goal, 2) if avance_goal is not None else None,
                }
            )

        return monthly_rows

    def get_metrics(self, obj: Campaign):
        monthly = self.get_monthly_data(obj)
        total_tramites = monthly[-1]['acumulado'] if monthly else 0
        forecast = obj.forecast or 0
        goal_pct = self._as_float(obj.goal)
        goal_target = (goal_pct / 100.0 * forecast) if goal_pct else None
        expected_months = 8 if obj.campaign_type == Campaign.CAP else 4
        reported_months = len(monthly)
        avg_monthly = (total_tramites / reported_months) if reported_months else 0
        projection_total = avg_monthly * expected_months if reported_months else 0

        remaining_goal = (
            max(goal_target - total_tramites, 0)
            if goal_target is not None
            else None
        )
        remaining_forecast = max(forecast - total_tramites, 0)

        best_month = None
        if monthly:
            best = max(monthly, key=lambda item: item['tramites'])
            best_month = {
                'month': best['month'],
                'label': best['label'],
                'tramites': best['tramites'],
            }

        latest_month = monthly[-1] if monthly else None

        trend_delta = None
        if reported_months >= 2:
            trend_delta = latest_month['tramites'] - monthly[-2]['tramites']

        return {
            'total_tramites': total_tramites,
            'forecast': forecast,
            'avance_pct': round(self._as_float(obj.avance), 2),
            'goal_pct': goal_pct,
            'goal_target': round(goal_target, 2) if goal_target is not None else None,
            'goal_met': (total_tramites >= goal_target) if goal_target is not None else None,
            'remaining_to_goal': round(remaining_goal, 2) if remaining_goal is not None else None,
            'remaining_to_forecast': round(remaining_forecast, 2),
            'reported_months': reported_months,
            'expected_months': expected_months,
            'average_monthly': round(avg_monthly, 2),
            'projection_total': round(projection_total, 2),
            'projection_gap': round(max(forecast - projection_total, 0), 2),
            'best_month': best_month,
            'latest_month': latest_month,
            'trend_delta': trend_delta,
        }

    def get_charts(self, obj: Campaign):
        monthly = self.get_monthly_data(obj)
        return {
            'labels': [row['label'] for row in monthly],
            'tramites': [row['tramites'] for row in monthly],
            'acumulado': [row['acumulado'] for row in monthly],
            'avance_pct': [row['avance_pct'] for row in monthly],
            'avance_vs_goal_pct': [
                row['avance_vs_goal_pct'] for row in monthly
            ],
        }

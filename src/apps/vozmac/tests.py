from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.vozmac.models import PaqueteEncuesta, RespuestaEncuesta


class VozmacAPITests(TestCase):
    def setUp(self):
        self.batch = PaqueteEncuesta.objects.create(
            file_name='demo.gz',
            file_hash='hash-demo-001',
            mac='123456',
            device_id='A',
            record_count=1,
        )

    def _create_response(
        self,
        created_at,
        visita=1,
        p1=4,
        p2=4,
        p3=4,
        p4=4,
        device_id='290101',
        mac='123456',
    ):
        return RespuestaEncuesta.objects.create(
            batch=self.batch,
            device_id=device_id,
            p0_tipo_visita=visita,
            p1_claridad_info=p1,
            p2_amabilidad=p2,
            p3_instalaciones=p3,
            p4_tiempo_espera=p4,
            created_at=created_at,
            mac=mac,
            distrito=1,
        )

    def test_motivo_endpoint_returns_counts(self):
        now = timezone.now()
        self._create_response(now, visita=1)
        self._create_response(now - timedelta(days=1), visita=2)

        response = self.client.get(reverse('api_motivo'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        totals = {item['p0_tipo_visita']: item['total'] for item in data}
        self.assertEqual(totals.get(1), 1)
        self.assertEqual(totals.get(2), 1)

    def test_satisfaccion_endpoint_fallbacks_to_latest_year(self):
        last_year = timezone.now().year - 1
        created_at = timezone.now().replace(year=last_year, month=5, day=10)
        self._create_response(created_at, p1=5, p2=5, p3=4, p4=4)

        response = self.client.get(reverse('api_satisfaccion'))
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['year'], last_year)
        self.assertGreater(payload['total_responses'], 0)
        self.assertIn('p1_claridad_info', payload['by_question'])
        self.assertEqual(payload['by_question']['p1_claridad_info']['average'], 5.0)

    def test_seguimiento_endpoint_has_monthly_data(self):
        now = timezone.now()
        self._create_response(now.replace(month=1, day=15))
        self._create_response(now.replace(month=2, day=15), p1=3)

        response = self.client.get(reverse('api_seguimiento'))
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload['labels']), 12)
        self.assertTrue(any(series['data'] for series in payload['datasets']))

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.kpi.models import Campaign, TramiteMensual


class CampaignAPITests(APITestCase):
    def setUp(self):
        self.cap = Campaign.objects.create(
            year=2025,
            campaign_type=Campaign.CAP,
            goal=90,
            forecast=1000,
        )
        TramiteMensual.objects.create(campaign=self.cap, month=1, tramites=120)
        TramiteMensual.objects.create(campaign=self.cap, month=2, tramites=150)
        TramiteMensual.objects.create(campaign=self.cap, month=3, tramites=200)

        self.cai = Campaign.objects.create(
            year=2024,
            campaign_type=Campaign.CAI,
            goal=85,
            forecast=400,
        )
        TramiteMensual.objects.create(campaign=self.cai, month=9, tramites=80)

        self.list_url = reverse('kpi-list')

    def test_list_campaigns_returns_metrics(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 2)

        cap_payload = next(item for item in response.data if item['year'] == 2025)
        self.assertIn('monthly_data', cap_payload)
        self.assertEqual(cap_payload['monthly_data'][0]['month'], 1)
        self.assertIn('metrics', cap_payload)
        self.assertGreater(cap_payload['metrics']['total_tramites'], 0)
        self.assertIn('charts', cap_payload)
        self.assertEqual(len(cap_payload['charts']['tramites']), len(cap_payload['monthly_data']))

    def test_filter_by_year_and_type(self):
        response = self.client.get(self.list_url, {'year': 2024, 'type': 'CAI'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['campaign_type'], Campaign.CAI)
        self.assertEqual(response.data[0]['year'], 2024)

    def test_invalid_year_returns_error(self):
        response = self.client.get(self.list_url, {'year': 'dos mil'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('year', response.data)

    def test_invalid_type_returns_error(self):
        response = self.client.get(self.list_url, {'type': 'XYZ'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('type', response.data)

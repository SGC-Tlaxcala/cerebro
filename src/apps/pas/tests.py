from datetime import date
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.pas.models import Plan, Accion

User = get_user_model()


class PASAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.plan = Plan.objects.create(
            folio=1,
            fecha_llenado=date.today(),
            user=self.user,
            documento=1,
            desc_cnc="Test Plan",
            analisis="Test Analysis",
        )
        self.action = Accion.objects.create(
            plan=self.plan,
            accion="Test Action",
            responsable=self.user,
            fecha_fin=date.today(),
        )

    def test_index_public_access(self):
        """Test that the index page is accessible without login."""
        response = self.client.get(reverse("pas:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Control de Planes de Acción")
        # Ensure 'Agregar plan' button is NOT present for anonymous
        self.assertNotContains(response, 'href="/pas/add/"')

    def test_detail_public_access(self):
        """Test that the plan detail page is accessible without login."""
        response = self.client.get(reverse("pas:detalle", args=[self.plan.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.plan.desc_cnc)

    def test_add_plan_protected(self):
        """Test that adding a plan requires login."""
        response = self.client.get(reverse("pas:add"))
        self.assertNotEqual(response.status_code, 200)
        # Should redirect to login
        self.assertEqual(response.status_code, 302)

    def test_edit_plan_protected(self):
        """Test that editing a plan requires login."""
        response = self.client.get(reverse("pas:plan-edit", args=[self.plan.pk]))
        self.assertEqual(response.status_code, 302)

    def test_summary_partial_public_access(self):
        """Test that plan summary partial is accessible."""
        response = self.client.get(reverse("pas:plan-summary", args=[self.plan.pk]))
        self.assertEqual(response.status_code, 200)
        # Ensure 'Editar plan' button is NOT present
        self.assertNotContains(response, "Editar plan")

    def test_activities_partial_public_access(self):
        """Test that activities list partial is accessible."""
        response = self.client.get(reverse("pas:plan-activities", args=[self.plan.pk]))
        self.assertEqual(response.status_code, 200)
        # Ensure 'Agregar actividad' button is NOT present
        self.assertNotContains(response, "Agregar actividad")
        # Ensure 'Editar' button is NOT present
        self.assertNotContains(response, "Editar")

    def test_plan_siglas(self):
        """Test the siglas property of Plan model."""
        plan_cnc = Plan(documento=1)  # CNC
        self.assertEqual(plan_cnc.siglas, "CNC")
        plan_pcm = Plan(documento=2)  # PCM
        self.assertEqual(plan_pcm.siglas, "PCM")
        plan_unknown = Plan(documento=99)
        self.assertEqual(plan_unknown.siglas, "N/A")

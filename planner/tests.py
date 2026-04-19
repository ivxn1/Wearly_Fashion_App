from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import CustomerProfileModel
from outfits.models import Outfit
from planner.models import PlanEntry

UserModel = get_user_model()


class PlanEntryModelTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.get(pk=1)
        self.outfit = Outfit.objects.create(
            title="Plan Outfit",
            occasion="Work",
            user=self.user,
        )

    def test_plan_entry_str_contains_date_and_outfit(self):
        target_date = date.today() + timedelta(days=500)
        entry = PlanEntry.objects.create(
            date=target_date,
            outfit=self.outfit,
            user=self.user,
        )
        self.assertIn(str(target_date), str(entry))
        self.assertIn("Plan Outfit", str(entry))

    def test_unique_constraint_one_plan_per_date_per_user(self):
        target_date = date.today() + timedelta(days=600)
        PlanEntry.objects.create(
            date=target_date,
            outfit=self.outfit,
            user=self.user,
        )
        with self.assertRaises(IntegrityError):
            PlanEntry.objects.create(
                date=target_date,
                outfit=self.outfit,
                user=self.user,
            )

    def test_outfit_protect_on_delete(self):
        PlanEntry.objects.create(
            date=date.today() + timedelta(days=700),
            outfit=self.outfit,
            user=self.user,
        )
        with self.assertRaises(Exception):
            self.outfit.delete()

    def test_plan_entries_ordered_by_date(self):
        d1 = date.today() + timedelta(days=800)
        d2 = date.today() + timedelta(days=801)
        PlanEntry.objects.create(date=d2, outfit=self.outfit, user=self.user)
        PlanEntry.objects.create(date=d1, outfit=self.outfit, user=self.user)
        entries = list(PlanEntry.objects.filter(user=self.user, date__gte=d1))
        self.assertEqual(entries[0].date, d1)
        self.assertEqual(entries[1].date, d2)


class PlannerViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.get(pk=1)
        self.user.set_password("testpass123")
        self.user.save()
        CustomerProfileModel.objects.get_or_create(
            user=self.user,
            defaults={"first_name": "Test", "last_name": "User"},
        )
        self.client = Client()
        self.client.login(email=self.user.email, password="testpass123")

    def test_planner_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("planner:list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_planner_list_returns_200(self):
        response = self.client.get(reverse("planner:list"))
        self.assertEqual(response.status_code, 200)

    def test_trigger_digest_rejects_non_premium(self):
        self.user.is_premium = False
        self.user.save()
        response = self.client.post(reverse("planner:trigger_digest"))
        self.assertEqual(response.status_code, 302)

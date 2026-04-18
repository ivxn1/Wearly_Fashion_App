from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import CustomerProfileModel
from outfits.models import Outfit, OutfitGarment
from wardrobe.models import Brand, Garment

UserModel = get_user_model()


class OutfitModelTest(TestCase):

    def setUp(self):
        self.user = UserModel.objects.get(pk=1)
        self.brand, _ = Brand.objects.get_or_create(name="OutfitBrand")

    def test_outfit_str_contains_title_and_occasion(self):
        outfit = Outfit.objects.create(
            title="Summer Vibes", occasion="Beach", season="summer",
            user=self.user,
        )
        self.assertIn("Summer Vibes", str(outfit))
        self.assertIn("Beach", str(outfit))

    def test_outfit_garment_unique_constraint(self):
        outfit = Outfit.objects.create(
            title="Test Outfit", occasion="Casual", user=self.user,
        )
        garment = Garment.objects.create(
            title="Test Garment", brand=self.brand, category="tshirt",
            color="Red", user=self.user,
        )
        OutfitGarment.objects.create(outfit=outfit, garment=garment)
        with self.assertRaises(IntegrityError):
            OutfitGarment.objects.create(outfit=outfit, garment=garment)

    def test_garment_protect_on_delete_from_outfit(self):
        outfit = Outfit.objects.create(
            title="Protect Test", occasion="Work", user=self.user,
        )
        garment = Garment.objects.create(
            title="Protected Garment", brand=self.brand, category="shirt",
            color="White", user=self.user,
        )
        OutfitGarment.objects.create(outfit=outfit, garment=garment)
        with self.assertRaises(Exception):
            garment.delete()

    def test_outfit_default_season_is_all(self):
        outfit = Outfit.objects.create(
            title="No Season Outfit", occasion="Daily", user=self.user,
        )
        self.assertEqual(outfit.season, "")


class OutfitViewTest(TestCase):

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

    def test_outfit_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("outfits:outfits_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_outfit_list_returns_200(self):
        response = self.client.get(reverse("outfits:outfits_list"))
        self.assertEqual(response.status_code, 200)

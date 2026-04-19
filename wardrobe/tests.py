from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.timezone import now

from accounts.models import CustomerProfileModel
from wardrobe.models import Brand, Garment
from wardrobe.validators import ImageSizeValidator

UserModel = get_user_model()


class BrandModelTest(TestCase):
    def test_brand_str_returns_name(self):
        brand = Brand.objects.create(name="TestBrandStr")
        self.assertEqual(str(brand), "TestBrandStr")

    def test_brand_name_is_unique(self):
        Brand.objects.create(name="UniqueBrand")
        with self.assertRaises(Exception):
            Brand.objects.create(name="UniqueBrand")


class GarmentModelTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.get(pk=1)
        self.brand, _ = Brand.objects.get_or_create(name="TestBrand")

    def test_garment_str_representation(self):
        garment = Garment.objects.create(
            title="Black Tee",
            brand=self.brand,
            category="tshirt",
            color="Black",
            user=self.user,
        )
        self.assertIn("Black Tee", str(garment))
        self.assertIn("TestBrand", str(garment))

    def test_garment_ordering_is_newest_first(self):
        g1 = Garment.objects.create(
            title="First",
            brand=self.brand,
            category="tshirt",
            color="Red",
            user=self.user,
        )
        g2 = Garment.objects.create(
            title="Second",
            brand=self.brand,
            category="jeans",
            color="Blue",
            user=self.user,
        )
        garments = list(Garment.objects.filter(pk__in=[g1.pk, g2.pk]))
        self.assertEqual(garments[0].pk, g2.pk)

    def test_garment_default_season_is_all(self):
        garment = Garment.objects.create(
            title="No Season",
            brand=self.brand,
            category="shirt",
            color="White",
            user=self.user,
        )
        self.assertEqual(garment.season, "")

    def test_brand_protect_on_delete(self):
        brand = Brand.objects.create(name="ProtectBrand")
        Garment.objects.create(
            title="Protected",
            brand=brand,
            category="coat",
            color="Grey",
            user=self.user,
        )
        with self.assertRaises(Exception):
            brand.delete()

    def test_garment_created_at_date_generated_automatically(self):
        before = now()
        garment = Garment.objects.create(
            title="No Season",
            brand=self.brand,
            category="shirt",
            color="White",
            user=self.user,
        )
        after = now()
        self.assertTrue(before <= garment.created_at <= after)


class GarmentSlugTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.get(pk=1)
        self.brand, _ = Brand.objects.get_or_create(name="SlugBrand")

    def test_slug_is_auto_generated(self):
        garment = Garment.objects.create(
            title="Cool Shirt",
            brand=self.brand,
            category="tshirt",
            color="Black",
            user=self.user,
        )
        self.assertEqual(garment.slug, "cool-shirt-slugbrand")

    def test_duplicate_slug_gets_suffix(self):
        Garment.objects.create(
            title="Cool Shirt",
            brand=self.brand,
            category="tshirt",
            color="Black",
            user=self.user,
        )
        second = Garment.objects.create(
            title="Cool Shirt",
            brand=self.brand,
            category="tshirt",
            color="White",
            user=self.user,
        )
        self.assertEqual(second.slug, "cool-shirt-slugbrand-1")


class ImageSizeValidatorTest(TestCase):
    def test_rejects_file_over_5mb(self):
        validator = ImageSizeValidator("Too big")

        class FakeImage:
            size = 6 * 1024 * 1024

        with self.assertRaises(ValidationError):
            validator(FakeImage())

    def test_accepts_file_under_5mb(self):
        validator = ImageSizeValidator("Too big")

        class FakeImage:
            size = 1 * 1024 * 1024

        try:
            validator(FakeImage())
        except ValidationError:
            self.fail("Validator raised ValidationError on a small file")


class GarmentViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.get(pk=1)
        self.user.set_password("testpass123")
        self.user.save()
        # Ensure profile exists for template rendering
        CustomerProfileModel.objects.get_or_create(
            user=self.user,
            defaults={"first_name": "Test", "last_name": "User"},
        )
        self.client = Client()
        self.client.login(email=self.user.email, password="testpass123")
        self.brand, _ = Brand.objects.get_or_create(name="ViewBrand")

    def test_garment_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("wardrobe:garment_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_normal_user_reaches_max_garment_limit(self):
        fresh_user = UserModel.objects.create_user(
            email="limittest@test.com",
            password="testpass123",
        )
        CustomerProfileModel.objects.get_or_create(
            user=fresh_user,
            defaults={"first_name": "Limit", "last_name": "Tester"},
        )
        self.client.login(email="limittest@test.com", password="testpass123")

        for i in range(10):
            Garment.objects.create(
                title=f"Cool Shirt {i}",
                brand=self.brand,
                category="tshirt",
                color="Black",
                user=fresh_user,
            )

        response = self.client.get(reverse("wardrobe:garment_create"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("wardrobe:garment_list"))

    def test_garment_detail_returns_200(self):
        garment = Garment.objects.create(
            title="Detail Test",
            brand=self.brand,
            category="shirt",
            color="Blue",
            user=self.user,
        )
        response = self.client.get(
            reverse("wardrobe:garment_details", kwargs={"slug": garment.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_brand_delete_blocked_when_has_garments(self):
        brand = Brand.objects.create(name="BlockDeleteBrand")
        Garment.objects.create(
            title="Blocking",
            brand=brand,
            category="jeans",
            color="Black",
            user=self.user,
        )
        response = self.client.post(
            reverse("wardrobe:brand_delete", kwargs={"pk": brand.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Brand.objects.filter(pk=brand.pk).exists())

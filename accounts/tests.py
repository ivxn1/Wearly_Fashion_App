from django.contrib.auth import get_user_model
from django.core import signing
from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import CustomerProfileModel, Wishlist, FavouriteOutfits
from accounts.tasks import PREMIUM_SALT

UserModel = get_user_model()


class CustomerUserModelTest(TestCase):

    def test_create_user_with_email(self):
        user = UserModel.objects.create_user(
            email="newuser@wearly.app", password="securepass123"
        )
        self.assertEqual(user.email, "newuser@wearly.app")
        self.assertTrue(user.check_password("securepass123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email_raises(self):
        with self.assertRaises(ValueError):
            UserModel.objects.create_user(email="", password="pass123")

    def test_user_is_not_premium_by_default(self):
        user = UserModel.objects.create_user(
            email="default@wearly.app", password="pass123"
        )
        self.assertFalse(user.is_premium)

    def test_user_str_returns_email(self):
        user = UserModel.objects.create_user(
            email="str@wearly.app", password="pass123"
        )
        self.assertEqual(str(user), "str@wearly.app")


class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = UserModel.objects.create_user(
            email="profile@wearly.app", password="pass123"
        )
        # Signal auto-creates a profile, so update it
        self.profile = self.user.profile
        self.profile.first_name = "John"
        self.profile.last_name = "Doe"
        self.profile.save()

    def test_profile_get_profile_name(self):
        self.assertEqual(self.profile.get_profile_name(), "John Doe")

    def test_profile_created_by_signal(self):
        user = UserModel.objects.create_user(
            email="signal@wearly.app", password="pass123"
        )
        self.assertTrue(
            CustomerProfileModel.objects.filter(user=user).exists()
        )


class ActivatePremiumViewTest(TestCase):

    def setUp(self):
        self.user = UserModel.objects.get(pk=1)
        self.user.set_password("pass123")
        self.user.is_premium = False
        self.user.save()
        CustomerProfileModel.objects.get_or_create(
            user=self.user,
            defaults={"first_name": "Premium", "last_name": "User"},
        )
        self.client = Client()

    def test_valid_token_activates_premium(self):
        token = signing.dumps({"user_id": self.user.pk}, salt=PREMIUM_SALT)
        response = self.client.get(
            reverse("activate-premium", kwargs={"token": token})
        )
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_premium)
        self.assertEqual(response.status_code, 302)

    def test_invalid_token_redirects_to_login(self):
        response = self.client.get(
            reverse("activate-premium", kwargs={"token": "bad-token"})
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_already_premium_user_stays_premium(self):
        self.user.is_premium = True
        self.user.save()
        token = signing.dumps({"user_id": self.user.pk}, salt=PREMIUM_SALT)
        self.client.get(
            reverse("activate-premium", kwargs={"token": token})
        )
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_premium)


class AuthViewTest(TestCase):

    def test_register_page_returns_200(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_login_page_returns_200(self):
        response = self.client.get(reverse("user-login"))
        self.assertEqual(response.status_code, 200)

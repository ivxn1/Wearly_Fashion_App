from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

UserModel = get_user_model()


class HomeViewTest(TestCase):

    def test_home_page_returns_200_for_anonymous(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)

    def test_home_page_returns_200_for_authenticated(self):
        user = UserModel.objects.get(pk=1)
        user.set_password("pass123")
        user.save()
        from accounts.models import CustomerProfileModel
        CustomerProfileModel.objects.get_or_create(
            user=user,
            defaults={"first_name": "Home", "last_name": "User"},
        )
        self.client.login(email=user.email, password="pass123")
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)


class Custom500Test(TestCase):

    def test_500_handler_returns_500(self):
        from core.views import custom_500
        factory = RequestFactory()
        request = factory.get("/")
        response = custom_500(request)
        self.assertEqual(response.status_code, 500)

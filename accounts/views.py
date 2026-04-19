from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core import signing
from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from accounts.forms import (
    CustomResetPasswordForm,
    UserProfileForm,
    UserRegistrationForm,
)
from accounts.models import CustomerProfileModel, FavouriteOutfits, Wishlist
from accounts.tasks import (
    PREMIUM_SALT,
    PREMIUM_TOKEN_MAX_AGE,
    send_premium_registration_email,
)
from core.mixin import IsUserOwnerMixin

UserModel = get_user_model()


class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = "accounts/user_registration.html"
    success_url = reverse_lazy("user-login")
    model = UserModel

    def form_valid(self, form):
        response = super().form_valid(form)
        member_group = Group.objects.filter(name="Member").first()
        if member_group:
            self.object.groups.add(member_group)
        return response


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.is_access_initial:
            return reverse_lazy(
                "user-profile-edit", kwargs={"pk": self.request.user.profile.pk}
            )
        return reverse_lazy("core:home")


class ProfileEditView(IsUserOwnerMixin, LoginRequiredMixin, UpdateView):
    template_name = "accounts/profile_create.html"

    def get_success_url(self):
        return reverse_lazy("user-profile", kwargs={"pk": self.object.pk})

    form_class = UserProfileForm
    model = CustomerProfileModel

    def form_valid(self, form):
        user = self.get_object().user
        if user.is_access_initial:
            user.is_access_initial = False
            user.save(update_fields=["is_access_initial"])
        return super().form_valid(form)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = "accounts/profile_detail.html"
    context_object_name = "profile"
    model = CustomerProfileModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object.user
        context["page_title"] = f"Profile - {self.object.get_profile_name()}"

        wishlist, _ = Wishlist.objects.get_or_create(user=user)
        wishlist_garments = wishlist.garments.select_related("brand").all()
        context["wishlist_garments"] = wishlist_garments
        context["wishlist_ids"] = set(wishlist_garments.values_list("id", flat=True))

        favourites, _ = FavouriteOutfits.objects.get_or_create(user=user)
        favourite_outfits = favourites.outfits.prefetch_related("garments").all()
        context["favourite_outfits"] = favourite_outfits
        context["favourites_ids"] = set(favourite_outfits.values_list("id", flat=True))

        return context


class BecomePremiumView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user

        if user.is_premium:
            messages.info(request, "You are already a Premium member!")
            return redirect("user-profile", pk=user.profile.pk)

        token = signing.dumps({"user_id": user.pk}, salt=PREMIUM_SALT)
        activation_url = request.build_absolute_uri(f"/activate-premium/{token}/")

        send_premium_registration_email.delay(user.pk, activation_url)

        messages.success(
            request,
            "A confirmation email has been sent! Check your inbox to activate Premium.",
        )
        return redirect("user-profile", pk=user.profile.pk)


class ActivatePremiumView(View):
    def get(self, request, token, *args, **kwargs):
        try:
            data = signing.loads(
                token, salt=PREMIUM_SALT, max_age=PREMIUM_TOKEN_MAX_AGE
            )
        except signing.BadSignature:
            messages.error(request, "Invalid or expired activation link.")
            return redirect("user-login")

        try:
            user = UserModel.objects.get(pk=data["user_id"])
        except UserModel.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("user-login")

        if user.is_premium:
            messages.info(request, "Your Premium account is already active!")
        else:
            user.is_premium = True
            user.save(update_fields=["is_premium"])
            premium_group = Group.objects.filter(name="Premium Member").first()
            if premium_group:
                user.groups.add(premium_group)
            messages.success(
                request, "Welcome to Wearly Premium! Your account has been upgraded."
            )

        return redirect("user-profile", pk=user.profile.pk)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    success_message = (
        "We've emailed you instructions for setting your password, "
        "if an account exists with the email you entered. You should receive them shortly."
        " If you don't receive an email, "
        "please make sure you've entered the address you registered with, and check your spam folder."
    )

    html_email_template_name = "accounts/password_reset_email.html"
    email_template_name = "accounts/password_reset_email.html"
    template_name = "accounts/password_reset.html"
    subject_template_name = "accounts/password_reset_subject.txt"
    success_url = reverse_lazy("user-login")
    form_class = CustomResetPasswordForm

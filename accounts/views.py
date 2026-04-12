from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls.base import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from accounts.forms import UserRegistrationForm, UserProfileForm
from accounts.models import CustomerProfileModel, Wishlist, FavouriteOutfits
from core.mixin import IsUserOwnerMixin

# Create your views here.
UserModel = get_user_model()

class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = "accounts/user_registration.html"
    success_url = reverse_lazy("user-login")
    model = UserModel

class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True
    def get_success_url(self):
        if self.request.user.is_access_initial:
            return reverse_lazy("user-profile-edit", kwargs={"pk": self.request.user.profile.pk})
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

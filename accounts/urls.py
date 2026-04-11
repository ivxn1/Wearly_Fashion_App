from django.contrib.auth.views import LogoutView
from django.urls.conf import path

from accounts.views import RegisterView, CustomLoginView, ProfileDetailView, ProfileEditView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="user-login"),
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="user-profile"),
    path("profile/<int:pk>/edit/", ProfileEditView.as_view(), name="user-profile-edit"),
    path("profile/logout/", LogoutView.as_view(), name="user-logout"),
]
from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
)
from django.urls.conf import path

from accounts.views import (
    ActivatePremiumView,
    BecomePremiumView,
    CustomLoginView,
    ProfileDetailView,
    ProfileEditView,
    RegisterView,
    ResetPasswordView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="user-login"),
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="user-profile"),
    path("profile/<int:pk>/edit/", ProfileEditView.as_view(), name="user-profile-edit"),
    path("profile/logout/", LogoutView.as_view(), name="user-logout"),
    path("become-premium/", BecomePremiumView.as_view(), name="become-premium"),
    path(
        "activate-premium/<str:token>/",
        ActivatePremiumView.as_view(),
        name="activate-premium",
    ),
    path("password-reset/", ResetPasswordView.as_view(), name="reset-password"),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="accounts/password-reset-confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        PasswordResetCompleteView.as_view(
            template_name="accounts/password-reset-complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "password-reset-done/",
        PasswordResetDoneView.as_view(
            template_name="accounts/password-reset-done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-change/",
        PasswordChangeView.as_view(
            template_name="accounts/password-change.html",
        ),
        name="password_change",
    ),
    path(
        "password-change-done/",
        PasswordChangeDoneView.as_view(
            template_name="accounts/password-change-done.html",
        ),
        name="password_change_done",
    ),
]

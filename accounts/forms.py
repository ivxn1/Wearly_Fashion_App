from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.forms.fields import CharField
from django.forms.models import ModelForm
from django.forms.widgets import ClearableFileInput, Select, Textarea, TextInput
from django.template import loader

from accounts.models import CustomerProfileModel
from accounts.tasks import send_password_reset_email

UserModel = get_user_model()


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = [
            "email",
        ]
        widgets = {
            "email": TextInput(attrs={"class": "form-control"}),
        }
        error_messages = {
            "email": {
                "required": "Email is required.",
                "unique": "A user with this email already exists.",
                "invalid": "Enter a valid email address.",
            },
        }


class UserProfileForm(ModelForm):
    class Meta:
        model = CustomerProfileModel
        fields = [
            "first_name",
            "last_name",
            "bio",
            "style_preference",
            "profile_picture",
            "location",
        ]
        widgets = {
            "first_name": TextInput(attrs={"class": "form-control"}),
            "last_name": TextInput(attrs={"class": "form-control"}),
            "bio": Textarea(attrs={"class": "form-control", "rows": 3}),
            "style_preference": Select(attrs={"class": "form-control"}),
            "profile_picture": ClearableFileInput(attrs={"class": "form-control-file"}),
            "location": TextInput(attrs={"class": "form-control"}),
        }

        error_messages = {
            "first_name": {
                "required": "First name is required.",
                "max_length": "First name cannot exceed 20 characters.",
            },
            "last_name": {
                "required": "Last name is required.",
                "max_length": "Last name cannot exceed 20 characters.",
            },
            "bio": {
                "max_length": "Bio cannot exceed 300 characters.",
            },
            "style_preference": {
                "invalid_choice": "Please select a valid style preference.",
            },
            "profile_picture": {
                "invalid_image": "Please upload a valid image file.",
            },
            "location": {
                "max_length": "Location cannot exceed 30 characters.",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"] = CharField(
            disabled=True,
            widget=TextInput(attrs={"class": "form-control"}),
            label="Email",
        )
        if self.instance and self.instance.pk:
            self.fields["email"].initial = self.instance.user.email


class CustomResetPasswordForm(PasswordResetForm):
    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        subject = loader.render_to_string(subject_template_name, context)
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
        else:
            html_email = None
        return send_password_reset_email.delay(
            subject=subject,
            message=body,
            from_email=from_email,
            recipient_list=[to_email],
            html_message=html_email,
        )

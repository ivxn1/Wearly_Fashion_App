from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from core.choices import StylePreferencesChoices


class CustomerUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomerUser(AbstractBaseUser, PermissionsMixin):
    objects = CustomerUserManager()

    email = models.EmailField(unique=True, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    is_access_initial = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email



class CustomerProfileModel(models.Model):
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    bio = models.CharField(max_length=300, blank=True, null=True)
    style_preference = models.CharField(choices=StylePreferencesChoices, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)

    def get_profile_name(self):
        return f"{self.first_name} {self.last_name}"


class Wishlist(models.Model):
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist",
    )
    garments = models.ManyToManyField(
        to="wardrobe.Garment",
        blank=True,
        related_name="wishlisted_by",
    )


class FavouriteOutfits(models.Model):
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favourites",
    )
    outfits = models.ManyToManyField(
        to="outfits.Outfit",
        blank=True,
        related_name="favourited_by",
    )

    class Meta:
        verbose_name_plural = "Favourite Outfits"


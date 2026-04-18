from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations

def seed_user(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL)
    Profile = apps.get_model("accounts", "CustomerProfileModel")

    user, created = User.objects.get_or_create(
        pk=1,
        defaults={
            "email": "seed@wearly.app",
            "is_active": True,
        },
    )

    user.password = make_password("demo123")
    user.save()

    Profile.objects.get_or_create(
        user=user,
        defaults={
            "first_name": "Demo",
            "last_name": "User",
            "bio": "Wearly sample account for demo purposes.",
            "location": "Sofia, Bulgaria",
        },
    )


def reverse_seed(apps, schema_editor):
    Profile = apps.get_model("accounts", "CustomerProfileModel")
    User = apps.get_model(settings.AUTH_USER_MODEL)
    Profile.objects.filter(user_id=1).delete()
    User.objects.filter(pk=1).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_favouriteoutfits_wishlist"),
    ]

    operations = [
        migrations.RunPython(seed_user, reverse_seed),
    ]

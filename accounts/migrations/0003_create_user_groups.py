from django.db import migrations


def create_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    member_group, _ = Group.objects.get_or_create(name="Member")
    premium_group, _ = Group.objects.get_or_create(name="Premium Member")

    # Members get standard CRUD on wardrobe, outfits, planner
    member_perms = Permission.objects.filter(
        content_type__app_label__in=["wardrobe", "outfits", "planner"],
    ).exclude(
        codename__in=["can_trigger_digest", "can_create_styleboard"],
    )
    member_group.permissions.set(member_perms)

    # Premium members get everything Members have + custom permissions + accounts access
    premium_perms = Permission.objects.filter(
        content_type__app_label__in=["wardrobe", "outfits", "planner", "accounts"],
    )
    premium_group.permissions.set(premium_perms)


def remove_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=["Member", "Premium Member"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_customeruser_is_access_initial"),
        ("contenttypes", "0002_remove_content_type_name"),
        ("auth", "0012_alter_user_first_name_max_length"),
        ("wardrobe", "0007_seed_comprehensive_data"),
        ("outfits", "0008_alter_outfit_season"),
        ("planner", "0004_alter_planentry_options"),
    ]

    operations = [
        migrations.RunPython(create_groups, remove_groups),
    ]

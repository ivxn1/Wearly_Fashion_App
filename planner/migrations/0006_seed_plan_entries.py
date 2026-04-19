from datetime import date, timedelta

from django.db import migrations


def seed_plan_entries(apps, schema_editor):
    """
    Seeds plan entries for the next 14 days with outfit references.
    Depends on outfits being already seeded.
    """
    Outfit = apps.get_model("outfits", "Outfit")
    PlanEntry = apps.get_model("planner", "PlanEntry")

    today = date.today()

    plan_entries_data = [
        {
            "date": today,
            "outfit_title": "Sunday Coffee Run",
            "note": (
                "Starting the day with a quick coffee run."
                " Keep it casual and comfortable."
            ),
        },
        {
            "date": today + timedelta(days=1),
            "outfit_title": "Business Casual Friday",
            "note": (
                "Important client meeting today. "
                "Need to look professional but approachable."
            ),
        },
        {
            "date": today + timedelta(days=2),
            "outfit_title": "Gym Workout Session",
            "note": (
                "Morning gym session before work."
                " Pack change of clothes for the office."
            ),
        },
        {
            "date": today + timedelta(days=3),
            "outfit_title": "Casual Weekend Brunch",
            "note": "Brunch plans with college friends at the new cafe downtown.",
        },
        {
            "date": today + timedelta(days=4),
            "outfit_title": "Evening Date Night",
            "note": "Anniversary dinner at 7 PM. Make sure to iron the shirt!",
        },
        {
            "date": today + timedelta(days=5),
            "outfit_title": "Winter City Walk",
            "note": "Weekend trip to the city. Forecast shows cold temperatures.",
        },
        {
            "date": today + timedelta(days=6),
            "outfit_title": "Summer Beach Day",
            "note": "Beach day with family! Remember to pack sunscreen and towels.",
        },
        {
            "date": today + timedelta(days=7),
            "outfit_title": "Formal Business Meeting",
            "note": "Quarterly review presentation. Need to make a strong impression.",
        },
        {
            "date": today + timedelta(days=8),
            "outfit_title": "Sunday Coffee Run",
            "note": "Lazy Sunday morning. Just grabbing groceries and relaxing at home.",
        },
        {
            "date": today + timedelta(days=9),
            "outfit_title": "Business Casual Friday",
            "note": "Team lunch today. Casual but still office-appropriate.",
        },
        {
            "date": today + timedelta(days=10),
            "outfit_title": "Casual Weekend Brunch",
            "note": "Working from home today but have a video call in the afternoon.",
        },
        {
            "date": today + timedelta(days=11),
            "outfit_title": "Gym Workout Session",
            "note": "Evening workout class at 6 PM. Remember to bring water bottle.",
        },
        {
            "date": today + timedelta(days=12),
            "outfit_title": "Evening Date Night",
            "note": "Concert night! Wear comfortable but stylish outfit.",
        },
        {
            "date": today + timedelta(days=13),
            "outfit_title": "Winter City Walk",
            "note": "Museum visit planned. Expected to walk a lot, dress warmly.",
        },
    ]

    for entry_data in plan_entries_data:
        try:
            outfit = Outfit.objects.get(title=entry_data["outfit_title"], user_id=1)
            PlanEntry.objects.get_or_create(
                date=entry_data["date"],
                user_id=1,
                defaults={
                    "outfit": outfit,
                    "note": entry_data["note"],
                },
            )
        except Outfit.DoesNotExist:
            print(
                f"Outfit '{entry_data['outfit_title']}' not found. Skipping entry for {entry_data['date']}."
            )


def reverse_seed(apps, schema_editor):
    """
    Removes all seeded plan entries.
    """
    PlanEntry = apps.get_model("planner", "PlanEntry")
    PlanEntry.objects.filter(user_id=1).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("planner", "0005_planentry_user_alter_planentry_date_and_more"),
        ("outfits", "0011_seed_outfits"),
    ]

    operations = [
        migrations.RunPython(seed_plan_entries, reverse_seed),
    ]

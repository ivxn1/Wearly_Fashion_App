import os
import shutil

from django.conf import settings
from django.db import migrations
from PIL import Image


def copy_and_convert_image(source_path, dest_path):
    try:
        if os.path.exists(source_path):
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            source_ext = os.path.splitext(source_path)[1].lower()
            if source_ext in [".jpg", ".jpeg"]:
                shutil.copy2(source_path, dest_path)
            else:
                with Image.open(source_path) as img:
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    img.save(dest_path, "JPEG", quality=90)
            return True
    except Exception as e:
        print(f"Failed to copy/convert image from {source_path}: {e}")
    return False


def find_image_file(directory, base_name):
    if not os.path.exists(directory):
        return None
    extensions = [".jpg", ".jpeg", ".png", ".webp", ".avif"]
    for ext in extensions:
        path = os.path.join(directory, base_name + ext)
        if os.path.exists(path):
            return path
    try:
        for filename in os.listdir(directory):
            if filename.lower().startswith(base_name.lower()):
                return os.path.join(directory, filename)
    except Exception:
        pass
    return None


OUTFIT_IMAGE_MAP = {
    "casual_weekend_brunch": "casual",
    "business_casual_friday": "business",
    "summer_beach_day": "summer",
    "evening_date_night": "evening_date",
    "winter_city_walk": "winter",
    "gym_workout_session": "workout",
    "sunday_coffee_run": "sunday",
    "formal_business_meeting": "formal",
}

OUTFIT_GARMENT_MAPPINGS = [
    ("Casual Weekend Brunch", "classic-white-t-shirt-uniqlo"),
    ("Casual Weekend Brunch", "501-original-fit-jeans-levis"),
    ("Casual Weekend Brunch", "stan-smith-classics-adidas"),
    ("Casual Weekend Brunch", "wayfarer-sunglasses-tommy-hilfiger"),
    ("Business Casual Friday", "oxford-button-down-shirt-zara"),
    ("Business Casual Friday", "tailored-chino-trousers-hm"),
    ("Business Casual Friday", "chelsea-leather-boots-zara"),
    ("Business Casual Friday", "classic-leather-belt-tommy-hilfiger"),
    ("Summer Beach Day", "black-graphic-tee-nike"),
    ("Summer Beach Day", "chino-shorts-uniqlo"),
    ("Summer Beach Day", "leather-slide-sandals-hm"),
    ("Summer Beach Day", "aviator-sunglasses-ralph-lauren"),
    ("Evening Date Night", "navy-blue-polo-shirt-ralph-lauren"),
    ("Evening Date Night", "slim-fit-dark-wash-jeans-zara"),
    ("Evening Date Night", "chelsea-leather-boots-zara"),
    ("Evening Date Night", "reversible-belt-calvin-klein"),
    ("Winter City Walk", "merino-wool-sweater-uniqlo"),
    ("Winter City Walk", "wool-blend-dress-trousers-zara"),
    ("Winter City Walk", "down-puffer-coat-north-face"),
    ("Winter City Walk", "waterproof-hiking-boots-north-face"),
    ("Winter City Walk", "cashmere-wool-scarf-uniqlo"),
    ("Gym Workout Session", "black-graphic-tee-nike"),
    ("Gym Workout Session", "athletic-training-shorts-nike"),
    ("Gym Workout Session", "ultraboost-running-shoes-adidas"),
    ("Sunday Coffee Run", "classic-grey-hoodie-nike"),
    ("Sunday Coffee Run", "501-original-fit-jeans-levis"),
    ("Sunday Coffee Run", "air-max-90-sneakers-nike"),
    ("Sunday Coffee Run", "canvas-tote-bag-uniqlo"),
    ("Formal Business Meeting", "cable-knit-sweater-hm"),
    ("Formal Business Meeting", "wool-blend-dress-trousers-zara"),
    ("Formal Business Meeting", "wool-overcoat-zara"),
    ("Formal Business Meeting", "chelsea-leather-boots-zara"),
    ("Formal Business Meeting", "leather-messenger-bag-zara"),
]


def seed_outfits(apps, schema_editor):
    Outfit = apps.get_model("outfits", "Outfit")
    OutfitGarment = apps.get_model("outfits", "OutfitGarment")
    Garment = apps.get_model("wardrobe", "Garment")

    media_root = settings.MEDIA_ROOT
    outfits_dir = os.path.join(media_root, "outfits")
    os.makedirs(outfits_dir, exist_ok=True)
    sample_outfits_dir = os.path.join(settings.BASE_DIR, "static", "sample_images", "outfits")

    def get_outfit_image(title):
        slug = title.lower().replace(" ", "_").replace("'", "")
        dest_filename = f"{slug}.jpg"
        dest_path = os.path.join(outfits_dir, dest_filename)
        if os.path.exists(dest_path):
            return f"outfits/{dest_filename}"
        source_base = OUTFIT_IMAGE_MAP.get(slug)
        if source_base:
            source_path = find_image_file(sample_outfits_dir, source_base)
            if source_path and copy_and_convert_image(source_path, dest_path):
                return f"outfits/{dest_filename}"
        return ""

    # --- Outfits ---
    outfits_data = [
        {"title": "Casual Weekend Brunch", "occasion": "Brunch", "season": "spring", "notes": "Perfect relaxed look for a weekend brunch with friends. Comfortable yet put-together."},
        {"title": "Business Casual Friday", "occasion": "Office", "season": "autumn", "notes": "Smart casual office look suitable for client meetings and casual Fridays."},
        {"title": "Summer Beach Day", "occasion": "Beach", "season": "summer", "notes": "Light and breezy outfit perfect for a day at the beach or poolside relaxation."},
        {"title": "Evening Date Night", "occasion": "Date Night", "season": "autumn", "notes": "Elegant and sophisticated look for a romantic dinner date."},
        {"title": "Winter City Walk", "occasion": "Outdoor", "season": "winter", "notes": "Warm layered outfit for exploring the city during cold winter days."},
        {"title": "Gym Workout Session", "occasion": "Gym", "season": "all", "notes": "High-performance athletic wear for an intense workout session."},
        {"title": "Sunday Coffee Run", "occasion": "Casual", "season": "spring", "notes": "Quick and easy outfit for grabbing coffee or running errands."},
        {"title": "Formal Business Meeting", "occasion": "Business", "season": "winter", "notes": "Professional attire for important business meetings and presentations."},
    ]

    outfits = {}
    for data in outfits_data:
        data["image"] = get_outfit_image(data["title"])
        data["user_id"] = 1
        outfit, _ = Outfit.objects.get_or_create(title=data["title"], defaults=data)
        outfits[data["title"]] = outfit

    # --- Outfit-Garment links ---
    garments = {g.slug: g for g in Garment.objects.filter(user_id=1)}

    for outfit_title, garment_slug in OUTFIT_GARMENT_MAPPINGS:
        if outfit_title in outfits and garment_slug in garments:
            OutfitGarment.objects.get_or_create(
                outfit=outfits[outfit_title],
                garment=garments[garment_slug],
            )


def reverse_seed(apps, schema_editor):
    OutfitGarment = apps.get_model("outfits", "OutfitGarment")
    Outfit = apps.get_model("outfits", "Outfit")
    OutfitGarment.objects.filter(outfit__user_id=1).delete()
    Outfit.objects.filter(user_id=1).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("outfits", "0010_styleboard"),
        ("wardrobe", "0009_seed_brands_garments"),
    ]

    operations = [
        migrations.RunPython(seed_outfits, reverse_seed),
    ]

import io
import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from PIL import Image

from outfits.models import Outfit
from wardrobe.models import Garment

CATEGORY_FOLDER_MAP = {
    "tshirt": "tshirts", "shirt": "shirt", "sweater": "sweater",
    "hoodie": "hoodie", "jeans": "jeans", "trousers": "trousers",
    "shorts": "shorts", "skirt": "skirts", "jacket": "jacket",
    "coat": "coat", "sneakers": "sneakers", "boots": "boots",
    "sandals": "sandals", "bag": "bags", "belt": "belts",
    "scarf": "scarf", "sunglasses": "sunglasses",
}

GARMENT_IMAGE_MAP = {
    "classic-white-t-shirt-uniqlo": "tshirt1",
    "black-graphic-tee-nike": "tshirt2",
    "navy-blue-polo-shirt-ralph-lauren": "shirt",
    "oxford-button-down-shirt-zara": "shirt2",
    "merino-wool-sweater-uniqlo": "sweater1",
    "cable-knit-sweater-hm": "sweater2",
    "classic-grey-hoodie-nike": "hoodie1",
    "zip-up-tech-hoodie-adidas": "hoodie2",
    "501-original-fit-jeans-levis": "jeans1",
    "slim-fit-dark-wash-jeans-zara": "jeans2",
    "tailored-chino-trousers-hm": "trousers1",
    "wool-blend-dress-trousers-zara": "trousers2",
    "athletic-training-shorts-nike": "shorts1",
    "chino-shorts-uniqlo": "shorts2",
    "pleated-midi-skirt-zara": "skirts",
    "classic-denim-jacket-levis": "jacket1",
    "lightweight-bomber-jacket-zara": "jacket2",
    "waterproof-rain-jacket-north-face": "jacket3",
    "down-puffer-coat-north-face": "coat1",
    "wool-overcoat-zara": "coat2",
    "air-max-90-sneakers-nike": "sneakers1",
    "ultraboost-running-shoes-adidas": "sneakers2",
    "stan-smith-classics-adidas": "sneakers3",
    "chelsea-leather-boots-zara": "boots1",
    "waterproof-hiking-boots-north-face": "boots2",
    "leather-slide-sandals-hm": "sandals",
    "canvas-tote-bag-uniqlo": "bags1",
    "leather-messenger-bag-zara": "bags2",
    "classic-leather-belt-tommy-hilfiger": "belt1",
    "reversible-belt-calvin-klein": "belt2",
    "cashmere-wool-scarf-uniqlo": "scarf",
    "aviator-sunglasses-ralph-lauren": "sunglasses1",
    "wayfarer-sunglasses-tommy-hilfiger": "sunglasses2",
}

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


def read_and_convert_to_jpeg(source_path):
    try:
        with Image.open(source_path) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            buffer = io.BytesIO()
            img.save(buffer, "JPEG", quality=90)
            return buffer.getvalue()
    except Exception as e:
        print(f"  Failed to convert {source_path}: {e}")
    return None


class Command(BaseCommand):
    help = "Re-upload seed data images to the configured storage backend (Cloudinary, etc.)"

    def handle(self, *args, **options):
        sample_clothes_dir = os.path.join(settings.BASE_DIR, "static", "sample_images", "clothes")
        sample_outfits_dir = os.path.join(settings.BASE_DIR, "static", "sample_images", "outfits")

        self.stdout.write("Uploading garment images...")
        updated = 0
        for garment in Garment.objects.filter(user_id=1):
            source_base = GARMENT_IMAGE_MAP.get(garment.slug)
            if not source_base:
                continue
            folder = CATEGORY_FOLDER_MAP.get(garment.category, garment.category)
            source_dir = os.path.join(sample_clothes_dir, folder)
            source_path = find_image_file(source_dir, source_base)
            if not source_path:
                self.stdout.write(f"  Source not found for {garment.slug}")
                continue
            image_bytes = read_and_convert_to_jpeg(source_path)
            if not image_bytes:
                continue
            dest_path = f"wardrobe/{garment.slug}.jpg"
            if default_storage.exists(dest_path):
                default_storage.delete(dest_path)
            default_storage.save(dest_path, ContentFile(image_bytes))
            garment.image = dest_path
            garment.save(update_fields=["image"])
            updated += 1
            self.stdout.write(f"  Uploaded {garment.slug}")
        self.stdout.write(self.style.SUCCESS(f"Updated {updated} garment images."))

        self.stdout.write("Uploading outfit images...")
        updated = 0
        for outfit in Outfit.objects.filter(user_id=1):
            slug = outfit.title.lower().replace(" ", "_").replace("'", "")
            source_base = OUTFIT_IMAGE_MAP.get(slug)
            if not source_base:
                continue
            source_path = find_image_file(sample_outfits_dir, source_base)
            if not source_path:
                self.stdout.write(f"  Source not found for {outfit.title}")
                continue
            image_bytes = read_and_convert_to_jpeg(source_path)
            if not image_bytes:
                continue
            dest_path = f"outfits/{slug}.jpg"
            if default_storage.exists(dest_path):
                default_storage.delete(dest_path)
            default_storage.save(dest_path, ContentFile(image_bytes))
            outfit.image = dest_path
            outfit.save(update_fields=["image"])
            updated += 1
            self.stdout.write(f"  Uploaded {outfit.title}")
        self.stdout.write(self.style.SUCCESS(f"Updated {updated} outfit images."))

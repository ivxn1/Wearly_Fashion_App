import io
import os
from decimal import Decimal

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import migrations
from PIL import Image


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
    """Read an image file and return JPEG bytes."""
    try:
        with Image.open(source_path) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            buffer = io.BytesIO()
            img.save(buffer, "JPEG", quality=90)
            return buffer.getvalue()
    except Exception as e:
        print(f"Failed to read/convert image {source_path}: {e}")
    return None


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


def seed_brands_and_garments(apps, schema_editor):
    Brand = apps.get_model("wardrobe", "Brand")
    Garment = apps.get_model("wardrobe", "Garment")

    sample_clothes_dir = os.path.join(settings.BASE_DIR, "static", "sample_images", "clothes")

    def get_garment_image(slug, category):
        dest_path = f"wardrobe/{slug}.jpg"
        if default_storage.exists(dest_path):
            return dest_path
        folder = CATEGORY_FOLDER_MAP.get(category, category)
        source_base = GARMENT_IMAGE_MAP.get(slug)
        if source_base:
            source_dir = os.path.join(sample_clothes_dir, folder)
            source_path = find_image_file(source_dir, source_base)
            if source_path:
                image_bytes = read_and_convert_to_jpeg(source_path)
                if image_bytes:
                    saved_path = default_storage.save(dest_path, ContentFile(image_bytes))
                    return saved_path
        return ""

    # --- Brands ---
    brands_data = [
        {"name": "Nike", "website": "https://www.nike.com", "country": "United States"},
        {"name": "Adidas", "website": "https://www.adidas.com", "country": "Germany"},
        {"name": "Zara", "website": "https://www.zara.com", "country": "Spain"},
        {"name": "H&M", "website": "https://www.hm.com", "country": "Sweden"},
        {"name": "Levi's", "website": "https://www.levi.com", "country": "United States"},
        {"name": "Uniqlo", "website": "https://www.uniqlo.com", "country": "Japan"},
        {"name": "The North Face", "website": "https://www.thenorthface.com", "country": "United States"},
        {"name": "Ralph Lauren", "website": "https://www.ralphlauren.com", "country": "United States"},
        {"name": "Tommy Hilfiger", "website": "https://www.tommyhilfiger.com", "country": "United States"},
        {"name": "Calvin Klein", "website": "https://www.calvinklein.com", "country": "United States"},
    ]

    brands = {}
    for data in brands_data:
        brand, _ = Brand.objects.get_or_create(name=data["name"], defaults=data)
        brands[data["name"]] = brand

    # --- Garments ---
    garments_data = [
        {"title": "Classic White T-Shirt", "category": "tshirt", "brand": brands["Uniqlo"], "slug": "classic-white-t-shirt-uniqlo", "color": "White", "size": "M", "material": "Cotton", "season": "summer", "price": Decimal("14.99")},
        {"title": "Black Graphic Tee", "category": "tshirt", "brand": brands["Nike"], "slug": "black-graphic-tee-nike", "color": "Black", "size": "L", "material": "Cotton Blend", "season": "summer", "price": Decimal("29.99")},
        {"title": "Navy Blue Polo Shirt", "category": "shirt", "brand": brands["Ralph Lauren"], "slug": "navy-blue-polo-shirt-ralph-lauren", "color": "Navy Blue", "size": "M", "material": "Pique Cotton", "season": "spring", "price": Decimal("89.99")},
        {"title": "Oxford Button-Down Shirt", "category": "shirt", "brand": brands["Zara"], "slug": "oxford-button-down-shirt-zara", "color": "Light Blue", "size": "L", "material": "Oxford Cotton", "season": "spring", "price": Decimal("45.99")},
        {"title": "Merino Wool Sweater", "category": "sweater", "brand": brands["Uniqlo"], "slug": "merino-wool-sweater-uniqlo", "color": "Burgundy", "size": "M", "material": "Merino Wool", "season": "winter", "price": Decimal("49.99")},
        {"title": "Cable Knit Sweater", "category": "sweater", "brand": brands["H&M"], "slug": "cable-knit-sweater-hm", "color": "Cream", "size": "L", "material": "Acrylic Blend", "season": "winter", "price": Decimal("34.99")},
        {"title": "Classic Grey Hoodie", "category": "hoodie", "brand": brands["Nike"], "slug": "classic-grey-hoodie-nike", "color": "Heather Grey", "size": "L", "material": "French Terry", "season": "autumn", "price": Decimal("65.00")},
        {"title": "Zip-Up Tech Hoodie", "category": "hoodie", "brand": brands["Adidas"], "slug": "zip-up-tech-hoodie-adidas", "color": "Black", "size": "M", "material": "Recycled Polyester", "season": "autumn", "price": Decimal("79.99")},
        {"title": "501 Original Fit Jeans", "category": "jeans", "brand": brands["Levi's"], "slug": "501-original-fit-jeans-levis", "color": "Indigo", "size": "32x32", "material": "Denim", "season": "autumn", "price": Decimal("89.99")},
        {"title": "Slim Fit Dark Wash Jeans", "category": "jeans", "brand": brands["Zara"], "slug": "slim-fit-dark-wash-jeans-zara", "color": "Dark Blue", "size": "31x32", "material": "Stretch Denim", "season": "autumn", "price": Decimal("49.99")},
        {"title": "Tailored Chino Trousers", "category": "trousers", "brand": brands["H&M"], "slug": "tailored-chino-trousers-hm", "color": "Khaki", "size": "32", "material": "Cotton Twill", "season": "spring", "price": Decimal("34.99")},
        {"title": "Wool Blend Dress Trousers", "category": "trousers", "brand": brands["Zara"], "slug": "wool-blend-dress-trousers-zara", "color": "Charcoal", "size": "32", "material": "Wool Blend", "season": "winter", "price": Decimal("69.99")},
        {"title": "Athletic Training Shorts", "category": "shorts", "brand": brands["Nike"], "slug": "athletic-training-shorts-nike", "color": "Black", "size": "M", "material": "Dri-FIT Polyester", "season": "summer", "price": Decimal("35.00")},
        {"title": "Chino Shorts", "category": "shorts", "brand": brands["Uniqlo"], "slug": "chino-shorts-uniqlo", "color": "Navy", "size": "M", "material": "Cotton", "season": "summer", "price": Decimal("29.99")},
        {"title": "Pleated Midi Skirt", "category": "skirt", "brand": brands["Zara"], "slug": "pleated-midi-skirt-zara", "color": "Black", "size": "S", "material": "Polyester", "season": "spring", "price": Decimal("55.99")},
        {"title": "Classic Denim Jacket", "category": "jacket", "brand": brands["Levi's"], "slug": "classic-denim-jacket-levis", "color": "Medium Wash", "size": "L", "material": "Denim", "season": "spring", "price": Decimal("98.00")},
        {"title": "Lightweight Bomber Jacket", "category": "jacket", "brand": brands["Zara"], "slug": "lightweight-bomber-jacket-zara", "color": "Olive Green", "size": "M", "material": "Nylon", "season": "autumn", "price": Decimal("79.99")},
        {"title": "Waterproof Rain Jacket", "category": "jacket", "brand": brands["The North Face"], "slug": "waterproof-rain-jacket-north-face", "color": "Black", "size": "L", "material": "Gore-Tex", "season": "autumn", "price": Decimal("199.00")},
        {"title": "Down Puffer Coat", "category": "coat", "brand": brands["The North Face"], "slug": "down-puffer-coat-north-face", "color": "Black", "size": "L", "material": "Down Fill", "season": "winter", "price": Decimal("279.00")},
        {"title": "Wool Overcoat", "category": "coat", "brand": brands["Zara"], "slug": "wool-overcoat-zara", "color": "Camel", "size": "M", "material": "Wool Blend", "season": "winter", "price": Decimal("169.00")},
        {"title": "Air Max 90 Sneakers", "category": "sneakers", "brand": brands["Nike"], "slug": "air-max-90-sneakers-nike", "color": "White", "size": "US 10", "material": "Leather and Mesh", "season": "spring", "price": Decimal("129.99")},
        {"title": "Ultraboost Running Shoes", "category": "sneakers", "brand": brands["Adidas"], "slug": "ultraboost-running-shoes-adidas", "color": "Core Black", "size": "US 10", "material": "Primeknit", "season": "summer", "price": Decimal("179.99")},
        {"title": "Stan Smith Classics", "category": "sneakers", "brand": brands["Adidas"], "slug": "stan-smith-classics-adidas", "color": "White Green", "size": "US 9", "material": "Leather", "season": "spring", "price": Decimal("95.00")},
        {"title": "Chelsea Leather Boots", "category": "boots", "brand": brands["Zara"], "slug": "chelsea-leather-boots-zara", "color": "Brown", "size": "EU 43", "material": "Genuine Leather", "season": "autumn", "price": Decimal("119.00")},
        {"title": "Waterproof Hiking Boots", "category": "boots", "brand": brands["The North Face"], "slug": "waterproof-hiking-boots-north-face", "color": "Brown Black", "size": "US 10", "material": "Leather and Gore-Tex", "season": "winter", "price": Decimal("189.00")},
        {"title": "Leather Slide Sandals", "category": "sandals", "brand": brands["H&M"], "slug": "leather-slide-sandals-hm", "color": "Tan", "size": "US 10", "material": "Leather", "season": "summer", "price": Decimal("29.99")},
        {"title": "Canvas Tote Bag", "category": "bag", "brand": brands["Uniqlo"], "slug": "canvas-tote-bag-uniqlo", "color": "Natural", "size": "One Size", "material": "Canvas", "season": "summer", "price": Decimal("19.99")},
        {"title": "Leather Messenger Bag", "category": "bag", "brand": brands["Zara"], "slug": "leather-messenger-bag-zara", "color": "Black", "size": "Medium", "material": "Faux Leather", "season": "autumn", "price": Decimal("69.99")},
        {"title": "Classic Leather Belt", "category": "belt", "brand": brands["Tommy Hilfiger"], "slug": "classic-leather-belt-tommy-hilfiger", "color": "Brown", "size": "34", "material": "Genuine Leather", "season": "autumn", "price": Decimal("49.99")},
        {"title": "Reversible Belt", "category": "belt", "brand": brands["Calvin Klein"], "slug": "reversible-belt-calvin-klein", "color": "Black Brown", "size": "32", "material": "Leather", "season": "winter", "price": Decimal("59.99")},
        {"title": "Cashmere Wool Scarf", "category": "scarf", "brand": brands["Uniqlo"], "slug": "cashmere-wool-scarf-uniqlo", "color": "Grey", "size": "One Size", "material": "Cashmere Wool", "season": "winter", "price": Decimal("39.99")},
        {"title": "Aviator Sunglasses", "category": "sunglasses", "brand": brands["Ralph Lauren"], "slug": "aviator-sunglasses-ralph-lauren", "color": "Gold Brown", "size": "One Size", "material": "Metal Frame", "season": "summer", "price": Decimal("145.00")},
        {"title": "Wayfarer Sunglasses", "category": "sunglasses", "brand": brands["Tommy Hilfiger"], "slug": "wayfarer-sunglasses-tommy-hilfiger", "color": "Black", "size": "One Size", "material": "Acetate", "season": "summer", "price": Decimal("89.99")},
    ]

    for data in garments_data:
        data["image"] = get_garment_image(data["slug"], data["category"])
        data["user_id"] = 1
        Garment.objects.update_or_create(slug=data["slug"], defaults=data)


def reverse_seed(apps, schema_editor):
    Garment = apps.get_model("wardrobe", "Garment")
    Brand = apps.get_model("wardrobe", "Brand")
    Garment.objects.filter(user_id=1).delete()
    Brand.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("wardrobe", "0008_garment_user"),
        ("accounts", "0005_seed_user"),
    ]

    operations = [
        migrations.RunPython(seed_brands_and_garments, reverse_seed),
    ]

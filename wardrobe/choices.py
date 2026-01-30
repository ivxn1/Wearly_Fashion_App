from django.db import models


class SeasonChoices(models.TextChoices):
    ALL = '', 'All Seasons'
    SPRING = 'spring', 'Spring'
    SUMMER = 'summer', 'Summer'
    AUTUMN = 'autumn', 'Autumn'
    WINTER = 'winter', 'Winter'


class GarmentCategory(models.TextChoices):
    ALL = "", "All Categories"

    # Tops
    TSHIRT = "tshirt", "T-Shirt"
    SHIRT = "shirt", "Shirt"
    SWEATER = "sweater", "Sweater"
    HOODIE = "hoodie", "Hoodie"

    # Bottoms
    JEANS = "jeans", "Jeans"
    TROUSERS = "trousers", "Trousers"
    SHORTS = "shorts", "Shorts"
    SKIRT = "skirt", "Skirt"

    # Outerwear
    JACKET = "jacket", "Jacket"
    COAT = "coat", "Coat"

    # Footwear
    SNEAKERS = "sneakers", "Sneakers"
    BOOTS = "boots", "Boots"
    SANDALS = "sandals", "Sandals"

    # Accessories
    BAG = "bag", "Bag"
    BELT = "belt", "Belt"
    SCARF = "scarf", "Scarf"
    SUNGLASSES = "sunglasses", "Sunglasses"


# Grouped choices for forms/admin with headers
GARMENT_CATEGORY_CHOICES = [
    ('All', [
        (GarmentCategory.ALL, GarmentCategory.ALL.label),
    ]),
    ("Tops", [
        (GarmentCategory.TSHIRT, GarmentCategory.TSHIRT.label),
        (GarmentCategory.SHIRT, GarmentCategory.SHIRT.label),
        (GarmentCategory.SWEATER, GarmentCategory.SWEATER.label),
        (GarmentCategory.HOODIE, GarmentCategory.HOODIE.label),
    ]),
    ("Bottoms", [
        (GarmentCategory.JEANS, GarmentCategory.JEANS.label),
        (GarmentCategory.TROUSERS, GarmentCategory.TROUSERS.label),
        (GarmentCategory.SHORTS, GarmentCategory.SHORTS.label),
        (GarmentCategory.SKIRT, GarmentCategory.SKIRT.label),
    ]),
    ("Outerwear", [
        (GarmentCategory.JACKET, GarmentCategory.JACKET.label),
        (GarmentCategory.COAT, GarmentCategory.COAT.label),
    ]),
    ("Footwear", [
        (GarmentCategory.SNEAKERS, GarmentCategory.SNEAKERS.label),
        (GarmentCategory.BOOTS, GarmentCategory.BOOTS.label),
        (GarmentCategory.SANDALS, GarmentCategory.SANDALS.label),
    ]),
    ("Accessories", [
        (GarmentCategory.BAG, GarmentCategory.BAG.label),
        (GarmentCategory.BELT, GarmentCategory.BELT.label),
        (GarmentCategory.SCARF, GarmentCategory.SCARF.label),
        (GarmentCategory.SUNGLASSES, GarmentCategory.SUNGLASSES.label),
    ]),
]

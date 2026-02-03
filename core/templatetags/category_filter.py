from django import template

from wardrobe.choices import GARMENT_CATEGORY_CHOICES

register = template.Library()

@register.filter()
def category_filter(cat_value: str) -> str:
    """
    Return an emoji representation for a given category choice value.
    Example: 'tshirt' -> '👕'
    """
    emojis = {
        'tshirt': '👕',
        'shirt': '👔',
        'sweater': '🥼',
        'hoodie': '🧥',
        'jeans': '👖',
        'trousers': '👖',
        'shorts': '🩳',
        'skirt': '👗',
        'jacket': '🧥',
        'coat': '🧥',
        'sneakers': '👟',
        'boots': '🥾',
        'sandals': '👡',
        'bag': '👜',
        'belt': '👖',
        'scarf': '🧣',
        'sunglasses': '😎',
    }

    return emojis.get(cat_value, '👗')


@register.filter()
def category_display(cat_value: str) -> str:
    """
    Convert category choice value to its display label.
    Example: 'tshirt' -> 'T-Shirt'
    """
    category_dict = {}
    for group_name, choices in GARMENT_CATEGORY_CHOICES:
        for value, label in choices:
            category_dict[value] = label

    return category_dict.get(cat_value, cat_value)


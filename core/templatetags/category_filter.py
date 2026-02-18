"""
Custom template filters for garment category display.

This module provides filters for converting category values to
emoji representations and human-readable labels.
"""

from django import template

from wardrobe.choices import GARMENT_CATEGORY_CHOICES

register = template.Library()


@register.filter()
def category_filter(cat_value: str) -> str:
    """
    Return an emoji representation for a given category choice value.

    Args:
        cat_value: The category value (e.g., 'tshirt', 'jeans').

    Returns:
        str: An emoji representing the category, or '👗' as default.

    Example:
        {{ garment.category|category_filter }} -> '👕'
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

    Args:
        cat_value: The category value (e.g., 'tshirt').

    Returns:
        str: The human-readable label (e.g., 'T-Shirt').

    Example:
        {{ garment.category|category_display }} -> 'T-Shirt'
    """
    category_dict = {}
    for group_name, choices in GARMENT_CATEGORY_CHOICES:
        for value, label in choices:
            category_dict[value] = label

    return category_dict.get(cat_value, cat_value)

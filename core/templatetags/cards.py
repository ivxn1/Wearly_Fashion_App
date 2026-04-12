"""
Custom template tags for rendering card components.

This module provides inclusion tags for rendering various card types
used throughout the application (garment, outfit, plan, brand cards).
"""

from django import template

register = template.Library()


@register.inclusion_tag("core/partials/cards/garment_card.html", takes_context=True)
def garment_card(context, item):
    wishlist_ids = context.get("wishlist_ids") or set()
    return {
        "item": item,
        "is_wishlisted": item.id in wishlist_ids,
    }


@register.inclusion_tag("core/partials/cards/outfit_card.html", takes_context=True)
def outfit_card(context, item):
    favourites_ids = context.get("favourites_ids") or set()
    return {
        "item": item,
        "is_favourite": item.id in favourites_ids,
    }


@register.inclusion_tag("core/partials/cards/plans_card.html")
def plans_card(item):
    """
    Render a plan entry card component.

    Args:
        item: A PlanEntry model instance to display.

    Returns:
        dict: Context containing the plan item.
    """
    return {
        "item": item,
    }


@register.inclusion_tag("core/partials/cards/brand_card.html")
def brand_card(item):
    """
    Render a brand card component.

    Args:
        item: A Brand model instance to display.

    Returns:
        dict: Context containing the brand item.
    """
    return {
        "brand": item,
    }

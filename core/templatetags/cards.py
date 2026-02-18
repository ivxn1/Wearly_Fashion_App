"""
Custom template tags for rendering card components.

This module provides inclusion tags for rendering various card types
used throughout the application (garment, outfit, plan, brand cards).
"""

from django import template

register = template.Library()


@register.inclusion_tag('core/partials/cards/garment_card.html')
def garment_card(item):
    """
    Render a garment card component.

    Args:
        item: A Garment model instance to display.

    Returns:
        dict: Context containing the garment item.
    """
    return {
        'item': item,
    }


@register.inclusion_tag('core/partials/cards/outfit_card.html')
def outfit_card(item):
    """
    Render an outfit card component.

    Args:
        item: An Outfit model instance to display.

    Returns:
        dict: Context containing the outfit item.
    """
    return {
        'item': item,
    }


@register.inclusion_tag('core/partials/cards/plans_card.html')
def plans_card(item):
    """
    Render a plan entry card component.

    Args:
        item: A PlanEntry model instance to display.

    Returns:
        dict: Context containing the plan item.
    """
    return {
        'item': item,
    }


@register.inclusion_tag('core/partials/cards/brand_card.html')
def brand_card(item):
    """
    Render a brand card component.

    Args:
        item: A Brand model instance to display.

    Returns:
        dict: Context containing the brand item.
    """
    return {
        'brand': item,
    }


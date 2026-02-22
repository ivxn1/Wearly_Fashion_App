"""
Custom template tags for rendering collection sections.

This module provides an inclusion tag for rendering collection sections
with titles, items, and empty state handling.
"""

from django import template

register = template.Library()


@register.inclusion_tag("core/partials/collection_section.html")
def collection_section(
    title: str, items, section_type: str, icon: str, action_url: str = None
) -> dict:
    """
    Render a collection section with a title, items, type, and icon.

    Args:
        title: Section title displayed as header.
        items: Collection items to display (QuerySet or list).
        section_type: Type of collection ('wardrobe', 'outfits', 'plans', 'brands').
        icon: Emoji icon for empty state display.
        action_url: Optional custom URL for the empty state action button.

    Returns:
        dict: Context for rendering the collection section template.
    """
    empty_messages = {
        "wardrobe": "No wardrobe yet. Start building your wardrobe!",
        "outfits": "No outfits created yet. Mix and match your wardrobe!",
        "plans": "No upcoming plans yet. Schedule your outfits!",
        "brands": "No brands yet. Add your favorite fashion labels!",
    }

    action_texts = {
        "wardrobe": "+ Add Garment",
        "outfits": "+ Create Outfit",
        "plans": "+ Add Plan",
        "brands": "+ Add Brand",
    }

    return {
        "title": title,
        "items": items,
        "section_type": section_type,
        "icon": icon,
        "empty_message": empty_messages.get(section_type, "No items yet."),
        "action_url": action_url,
        "action_text": action_texts.get(section_type, "+ Add Item"),
    }

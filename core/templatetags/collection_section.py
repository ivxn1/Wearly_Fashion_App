"""
Custom template tags for rendering collection sections.

This module provides an inclusion tag for rendering collection sections
with titles, items, and empty state handling.
"""

from django import template

register = template.Library()


@register.inclusion_tag("core/partials/collection_section.html", takes_context=True)
def collection_section(
    context, title: str, items, section_type: str, icon: str, action_url: str = None
) -> dict:
    empty_messages = {
        "wardrobe": "No wardrobe yet. Start building your wardrobe!",
        "outfits": "No outfits created yet. Mix and match your wardrobe!",
        "plans": "No upcoming plans yet. Schedule your outfits!",
        "brands": "No brands yet. Add your favorite fashion labels!",
        "styleboards": "No style boards yet. Curate your looks!",
    }

    action_texts = {
        "wardrobe": "+ Add Garment",
        "outfits": "+ Create Outfit",
        "plans": "+ Add Plan",
        "brands": "+ Add Brand",
        "styleboards": "+ Create Style Board",
    }

    return {
        "title": title,
        "items": items,
        "section_type": section_type,
        "icon": icon,
        "empty_message": empty_messages.get(section_type, "No items yet."),
        "action_url": action_url,
        "action_text": action_texts.get(section_type, "+ Add Item"),
        "wishlist_ids": context.get("wishlist_ids") or set(),
        "favourites_ids": context.get("favourites_ids") or set(),
        "request": context.get("request"),
    }

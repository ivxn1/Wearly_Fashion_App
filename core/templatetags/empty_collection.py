"""
Custom template tags for rendering empty collection states.

This module provides an inclusion tag for displaying empty state
messages with optional action buttons.
"""

from django import template

register = template.Library()


@register.inclusion_tag("core/partials/empty_collection.html")
def empty_collection(
    emoji: str, message: str, action_url: str = None, action_text: str = None
) -> dict:
    """
    Render an empty collection message with an emoji and optional action button.

    Args:
        emoji: The emoji icon to display.
        message: The empty state message to show.
        action_url: Optional URL for the action button.
        action_text: Optional text for the action button (default: "+ Add Item").

    Returns:
        dict: Context for rendering the empty collection template.
    """
    return {
        "message": message,
        "emoji": emoji,
        "action_url": action_url,
        "action_text": action_text,
    }

from django import template

register = template.Library()

@register.inclusion_tag('core/partials/empty_collection.html')
def empty_collection(emoji: str, message: str, action_url: str = None, action_text: str = None):
    """
    Renders an empty collection message with an emoji and optional action button.

    Args:
        emoji: The emoji icon to display
        message: The empty state message
        action_url: Optional URL for the action button
        action_text: Optional text for the action button (default: "+ Add Item")
    """
    return {
        'message': message,
        'emoji': emoji,
        'action_url': action_url,
        'action_text': action_text,
    }

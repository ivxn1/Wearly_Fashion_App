from django import template

register = template.Library()

@register.inclusion_tag('core/partials/empty_collection.html')
def empty_collection(emoji: str, message: str):
    """
    Renders an empty collection message with an emoji.
    """
    return {
        'message': message,
        'emoji': emoji,
    }

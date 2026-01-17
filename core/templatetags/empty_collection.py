from django import template

register = template.Library()

@register.inclusion_tag('core/partials/empty_collection.html')
def empty_collection(emoji: str, message: str):
    return {
        'message': message,
        'emoji': emoji,
    }

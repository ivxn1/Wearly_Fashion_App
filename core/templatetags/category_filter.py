from django import template

register = template.Library()

@register.filter()
def category_filter(cat_name: str) -> str:
    emojis = {
        'Top': '👕',
        'Bottom': '👖',
        'Shoes': '👟',
        'Outerwear': '🧥',
        'Accessory': '👜',
        'Gloves': '🧤',
    }
    return emojis.get(cat_name, '')
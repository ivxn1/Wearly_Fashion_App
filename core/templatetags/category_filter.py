from django import template

register = template.Library()

@register.filter()
def category_filter(cat_name: str) -> str:

    # TODO: Replace with actual emojis or icons as needed

    emojis = {
        'Top': '👕',
        'Bottom': '👖',
        'Shoes': '👟',
        'Outerwear': '🧥',
        'Accessory': '👜',
        'Gloves': '🧤',
    }
    return emojis.get(cat_name, '')
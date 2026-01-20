from django import template

register = template.Library()

@register.inclusion_tag('core/partials/cards/garment_card.html')
def garment_card(item):
    """
    Renders a garment card.
    """
    return {
        'item': item,
    }

@register.inclusion_tag('core/partials/cards/outfit_card.html')
def outfit_card(item):
    """
    Renders an outfit card.
    """
    return {
        'item': item,
    }

@register.inclusion_tag('core/partials/cards/plans_card.html')
def plans_card(item):
    """
    Renders a plan card.
    """
    return {
        'item': item,
    }
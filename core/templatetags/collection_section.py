from django import template

register = template.Library()


@register.inclusion_tag('core/partials/collection_section.html')
def collection_section(title, items, section_type, icon):
    empty_messages = {
        'wardrobe': 'No wardrobe yet. Start building your wardrobe!',
        'outfits': 'No outfits created yet. Mix and match your wardrobe!',
        'plans': 'No upcoming plans yet. Schedule your outfits!',
    }

    return {
        'title': title,
        'items': items,
        'section_type': section_type,
        'icon': icon,
        'empty_message': empty_messages.get(section_type, 'No items yet.'),
    }

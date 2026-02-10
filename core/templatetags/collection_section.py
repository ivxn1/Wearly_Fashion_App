from django import template

register = template.Library()


@register.inclusion_tag('core/partials/collection_section.html')
def collection_section(title, items, section_type, icon, action_url=None):
    """
    Renders a collection section with a title, items, type, and icon.

    Args:
        title: Section title
        items: Collection items to display
        section_type: Type of collection ('wardrobe', 'outfits', 'plans', 'brands')
        icon: Emoji icon for empty state
        action_url: Optional custom URL for the empty state action button
    """
    empty_messages = {
        'wardrobe': 'No wardrobe yet. Start building your wardrobe!',
        'outfits': 'No outfits created yet. Mix and match your wardrobe!',
        'plans': 'No upcoming plans yet. Schedule your outfits!',
        'brands': 'No brands yet. Add your favorite fashion labels!',
    }

    action_texts = {
        'wardrobe': '+ Add Garment',
        'outfits': '+ Create Outfit',
        'plans': '+ Add Plan',
        'brands': '+ Add Brand',
    }

    return {
        'title': title,
        'items': items,
        'section_type': section_type,
        'icon': icon,
        'empty_message': empty_messages.get(section_type, 'No items yet.'),
        'action_url': action_url,
        'action_text': action_texts.get(section_type, '+ Add Item'),
    }

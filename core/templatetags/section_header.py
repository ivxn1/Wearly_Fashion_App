from django import template

register = template.Library()

@register.inclusion_tag('core/partials/section_header.html')
def section_header(title: str):
    """
    Renders a section header with a title.
    """
    return {
        'title': title,
    }
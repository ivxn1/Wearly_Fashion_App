from django import template

register = template.Library()

@register.inclusion_tag('core/partials/section_header.html')
def section_header(title: str):
    return {
        'title': title,
    }
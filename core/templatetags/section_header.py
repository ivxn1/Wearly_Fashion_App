"""
Custom template tags for rendering section headers.

This module provides an inclusion tag for rendering consistent
section header components throughout the application.
"""

from django import template

register = template.Library()


@register.inclusion_tag('core/partials/section_header.html')
def section_header(title: str) -> dict:
    """
    Render a section header with a title.

    Args:
        title: The section title to display.

    Returns:
        dict: Context containing the title for the template.
    """
    return {
        'title': title,
    }
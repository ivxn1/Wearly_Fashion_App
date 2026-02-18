"""
Custom template filters for text capitalization.

This module provides filters for capitalizing text in templates.
"""

from django.template import Library

register = Library()


@register.filter
def capitalize(value: str) -> str:
    """
    Capitalize each word in a string.

    Args:
        value: The input string to capitalize.

    Returns:
        str: The string with each word capitalized.

    Example:
        {{ "hello world"|capitalize }} -> "Hello World"
    """
    words = value.split(' ')
    capitalized_result = ' '.join(word.capitalize() for word in words)
    return capitalized_result
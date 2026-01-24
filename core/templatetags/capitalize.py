from django.template import Library

register = Library()

@register.filter
def capitalize(value:str) -> str:
    words = value.split(' ')
    capitalized_result = ' '.join(word.capitalize() for word in words)
    return capitalized_result
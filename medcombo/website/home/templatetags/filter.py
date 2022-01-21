from django.template.defaultfilters import stringfilter
from urllib.parse import unquote
from django import template

register = template.Library()

@register.filter(name='filter')
@stringfilter
def unquote_raw(value):
    key_value = value.replace(" ", "-")
    return unquote(key_value)
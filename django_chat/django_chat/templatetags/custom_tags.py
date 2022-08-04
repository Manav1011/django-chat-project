from django import template

register = template.Library()

@register.filter
def get_username(value):
    for i in value:
        return i
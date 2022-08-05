from django import template

register = template.Library()

@register.filter
def get_username(value):
    for i in value:
        return i
    
@register.filter
def get_pk(value):
    return value.pk

@register.filter
def is_viewed_count(value):
    value=value.filter(is_viewed=False)
    return value.count()


@register.filter
def get_id(value):
    for i in value:
        return i.id
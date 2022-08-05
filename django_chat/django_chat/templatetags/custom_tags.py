from django import template
import re

register = template.Library()

@register.filter
def get_username(value):
    for i in value:
        return i
    
@register.filter
def get_pk(value):
    return value.pk

@register.filter
def not_viewed(value,user):
    count=0
    for i in value:
        if user in i.viewed_by.all():
            pass
        else:
            count+=1
    return count


@register.filter
def get_id(value):
    for i in value:
        return i.id
    
    
@register.filter
def remove_unnecessary(value):
    s1="".join(c for c in value if c.isalpha())
    return s1

@register.filter
def is_online(value):
    for i in value:
        return i.first_name
    
from django import template
import re
from chats.models import PersonalChatRoom
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def get_username(value):
    for i in value:
        return i
    
@register.filter
def get_pk(value):
    return value.pk

@register.filter
def not_in_the_chat(value,user):
    chatobj=None
    for i in value:
        chatobj=i.chats.last()
            
    if user not in chatobj.viewed_by.all():
        return 'New Messages'
    else:
        return ''
    

@register.filter
def not_viewed(value,user):
    count=0
    if user in value.viewed_by.all():
        return ''
    else:
        count+=1
        return 'New Messages'

@register.filter
def get_counter(user):
    chatroom_obj=PersonalChatRoom.objects.filter(members=user)             
    room_partners={}
    for i in chatroom_obj:
        room_partners.update({i.members.all().exclude(username=user.username):i.members.all().exclude(username=user.username)})        
    RoomObjects={}
    for i in chatroom_obj:                
        RoomObjects.update({i:i})
    count=0
    for i in RoomObjects:
        for j in i.chats.all():
            if user in j.viewed_by.all():
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
    
    
@register.filter
def get_pk(value):
    return value.pk
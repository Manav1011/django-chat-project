from django.shortcuts import render
from .models import GroupChatRoom
import json


# Create your views here.

def group_chat_room(request,pk):
    qs=GroupChatRoom.objects.get(pk=pk)
    for i in qs.members_online.all():
        for j in qs.chats.all():
            j.viewed_by.add(i)
    return render(request,'groups/group_chat_room.html',{'qs':qs})
    
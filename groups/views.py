from django.shortcuts import render
from .models import GroupChatRoom
import json


# Create your views here.

def group_chat_room(request,pk):
    qs=GroupChatRoom.objects.get(pk=pk)
    return render(request,'groups/group_chat_room.html',{'qs':qs})
    
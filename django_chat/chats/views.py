from django.shortcuts import render
from .models import PersonalChatRoom
from django.http import JsonResponse,HttpResponse
import string
from django.shortcuts import redirect
from django.urls import reverse
import random
from django.contrib.auth.models import User
# Create your views here.

def create_personal_room(request,pk):
    user_id=pk
    current_user=request.user
    chat_partner=User.objects.get(id=user_id)   
    RoomObject=PersonalChatRoom.objects.new_or_get(request,chat_partner)
    context={
        'chat_partner':chat_partner,
        'RoomObject':RoomObject,
        
    }
    return render(request,'chats/personal_chat_room.html',context)
    


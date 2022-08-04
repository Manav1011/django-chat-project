from django.shortcuts import render
from .models import PersonalChatRoom
from django.http import JsonResponse
import string
import random
from django.contrib.auth.models import User
# Create your views here.

def create_personal_room(request):
    N=7
    Group_id = ''.join(random.choices(string.ascii_uppercase +string.digits, k=N))
    user_id=request.GET.get('id')
    current_user=request.user
    chat_partner=User.objects.get(id=user_id)   
    print(PersonalChatRoom.objects.new_or_get(request,chat_partner))
    
    return JsonResponse({'chat_parner':chat_partner.username,'current_user':current_user.username})

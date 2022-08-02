from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from chats.models import PersonalChat


@login_required
def home_view(request):    
    User=request.user
    chat_objects=PersonalChat.objects.get_personal_chats(User)    
    context={'chat_objects': chat_objects}   
    print(context) 
    return render(request,'home.html',context)
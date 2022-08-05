from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from chats.models import PersonalChat,PersonalChatRoom


@login_required
def home_view(request):    
    user=request.user
    chatroom_obj=PersonalChatRoom.objects.filter(members=user)        
    # chat_objects=PersonalChat.objects.get_personal_chats(User)   
    room_partners={}
    for i in chatroom_obj:
        room_partners.update({i.members.all().exclude(username=request.user.username):i.members.all().exclude(username=request.user.username)})        
    RoomObjects={}
    for i in chatroom_obj:                
        RoomObjects.update({i:i})
    combined=zip(room_partners,RoomObjects)
    context={'chatroom_objects': chatroom_obj,'sender':user,'parners':room_partners,'RoomObjects':RoomObjects,'combined':combined}   
    return render(request,'home.html',context)

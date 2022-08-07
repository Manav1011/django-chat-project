from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from chats.models import PersonalChat,PersonalChatRoom
from groups.models import GroupChat,GroupChatRoom
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from groups.forms import NewGroupForm


@login_required
def home_chat_view(request):    
    user=request.user
    chatroom_obj=PersonalChatRoom.objects.filter(members=user)             
    room_partners={}
    for i in chatroom_obj:
        room_partners.update({i.members.all().exclude(username=request.user.username):i.members.all().exclude(username=request.user.username)})        
    RoomObjects={}
    for i in chatroom_obj:                
        RoomObjects.update({i:i})
    combined=zip(room_partners,RoomObjects)
    context={'chatroom_objects': chatroom_obj,'sender':user,'parners':room_partners,'RoomObjects':RoomObjects,'combined':combined}   
    return render(request,'chat.html',context)


@login_required
def group_chat_view(request):    
    GroupObj=GroupChatRoom.objects.all().filter(members=request.user)
    form=NewGroupForm(request.POST or None)
    context={
        'GroupObj':GroupObj,
        'form':form
    }
    if request.method=='POST':
        object=form.save()        
        object.members.add(request.user)
        return HttpResponseRedirect(reverse('home_groups'))    
    
    return render(request,'groups.html',context)
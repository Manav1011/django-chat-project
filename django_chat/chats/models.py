from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError  
from django.dispatch import receiver
from django.db.models.signals import post_save,m2m_changed

# Create your models here.

class PersonalChatManager(models.Manager):
    def get_personal_chats(self,request,user):
        user=request.user
        chat_objects=self.get_queryset().filter(sender=user).values('reciever').distinct()
        qs={}
        for i in chat_objects:
            qs.update({f'object {i["reciever"]}':PersonalChat.objects.filter(reciever=i['reciever']).all().last()})    
        return qs

class PersonalChat(models.Model):
    chat=models.CharField(max_length=500,null=False,blank=False)
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    reciever=models.ForeignKey(User,related_name='reciever',on_delete=models.CASCADE,null=False,blank=False)
    timestamp=models.DateTimeField(auto_now_add=True)   
    is_viewed=models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.chat}'
    
    objects=PersonalChatManager()
    
@receiver(post_save,sender=PersonalChat)
def add_chat_to_chat_room(sender,instance,created,*args,**kwargs):
    if created:
        sender_=instance.sender
        reciever=instance.reciever
        chat_roomobj=PersonalChatRoom.objects.all()
        for i in chat_roomobj:
            if sender_ in i.members.all() and reciever in i.members.all():
                new_obj=i
                i.chats.add(instance)
            else:
                pass
        
        
class PersonalChatRoomManager(models.Manager):
    def new_or_get(self,request,chat_partner):
        current_user=request.user
        chat_partner=chat_partner
        chat_roomobj=PersonalChatRoom.objects.all()
        if chat_roomobj:        
            for i in chat_roomobj:
                if current_user in i.members.all() and chat_partner in i.members.all():
                    room_obj=i
                    print(room_obj)
                    return room_obj
                else:
                    room_obj=PersonalChatRoom.objects.create()        
                    room_obj.members.add(current_user)
                    room_obj.members.add(chat_partner)
                    return room_obj
        else:
            room_obj=PersonalChatRoom.objects.create()        
            room_obj.members.add(current_user)
            room_obj.members.add(chat_partner)
            return room_obj
        
    
class PersonalChatRoom(models.Model):    
    RoomName=models.CharField(max_length=255,blank=True,null=True)
    members=models.ManyToManyField(User)
    chats=models.ManyToManyField(PersonalChat,null=True,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    last_updated=models.DateTimeField(auto_now=True)
    
    objects=PersonalChatRoomManager()
    
@receiver(m2m_changed,sender=PersonalChatRoom.members.through)
def post_save_room(instance,sender,action,*args,**kwargs):
        print('created')    
        room_name=''
        print(instance.members.all())
        users=instance.members.all()
        for i in users:
            room_name+=i.username
        print(room_name)
        instance.RoomName=room_name
        instance.save()
    

            
    
    



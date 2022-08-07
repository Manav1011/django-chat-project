from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError  
from django.dispatch import receiver
from django.db.models.signals import post_save,m2m_changed

# Create your models here.


class GroupChat(models.Model):
    chat=models.CharField(max_length=500,null=False,blank=False)
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    reciever=models.ForeignKey(User,related_name='reciever',on_delete=models.CASCADE,null=False,blank=False)
    timestamp=models.DateTimeField(auto_now_add=True)   
    viewed_by=models.ManyToManyField(User,null=True,blank=True)
    
    def __str__(self):
        return f'{self.chat}'
    
# @receiver(post_save,sender=PersonalChat)
# def add_chat_to_chat_room(sender,instance,created,*args,**kwargs):
#     if created:
#         sender_=instance.sender
#         reciever=instance.reciever
#         chat_roomobj=PersonalChatRoom.objects.all()
#         for i in chat_roomobj:
#             if sender_ in i.members.all() and reciever in i.members.all():
#                 new_obj=i
#                 i.chats.add(instance)
#             else:
#                 pass
        
        
# class ChatRoomManager(models.Manager):
#     def new_or_get(self,request,chat_partner):
#         current_user=request.user
#         chat_partner=chat_partner
#         chat_roomobj=PersonalChatRoom.objects.all()
#         if chat_roomobj:        
#             for i in chat_roomobj:
#                 if current_user in i.members.all() and chat_partner in i.members.all():
#                     room_obj=i
#                     print(room_obj)
#                     return room_obj
#             room_obj=PersonalChatRoom.objects.create()        
#             room_obj.members.add(current_user)
#             room_obj.members.add(chat_partner)
#             return room_obj
#         else:
#             room_obj=PersonalChatRoom.objects.create()        
#             room_obj.members.add(current_user)
#             room_obj.members.add(chat_partner)
#             return room_obj
        
    
class GroupChatRoom(models.Model):    
    RoomName=models.CharField(max_length=255,blank=True,null=True)
    members=models.ManyToManyField(User,related_name='members')
    chats=models.ManyToManyField(GroupChat,null=True,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    last_updated=models.DateTimeField(auto_now=True)
    members_online=models.ManyToManyField(User,blank=True,null=True,related_name='online_members')
    
    # objects=PersonalChatRoomManager()
    
# @receiver(m2m_changed,sender=PersonalChatRoom.members.through)
# def post_save_room(instance,sender,action,*args,**kwargs):
#         print('created')    
#         room_name=''
#         print(instance.members.all())
#         users=instance.members.all()
#         for i in users:
#             room_name+=i.username
#         print(room_name)
#         instance.RoomName=room_name
#         instance.save()
    

            
    
    



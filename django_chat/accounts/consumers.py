import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from chats.models import PersonalChat,PersonalChatRoom
from groups.models import GroupChatRoom
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
import datetime
from django_chat.templatetags.custom_tags import remove_unnecessary

        
class PersonalChatConsumer(AsyncWebsocketConsumer):    
        
    def online_members(self,RoomName,user):
        self.RoomObj=PersonalChatRoom.objects.get(RoomName=RoomName)
        self.RoomObj.members_online.add(user)
    
    async def connect(self):               
        await self.accept()
        PersonalChatConsumer.user=self.scope['user']                     
        self.RoomObjName=self.scope["url_route"]["kwargs"]["RoomObjName"]
        await database_sync_to_async(self.online_members)(self.RoomObjName,self.scope['user'])
        PersonalChatConsumer.group_name=f'chat_{self.scope["url_route"]["kwargs"]["RoomName"]}'        
        await self.channel_layer.group_add(
            PersonalChatConsumer.group_name,
            self.channel_name
        )
    
    def offline_members(self,RoomName,user):        
        RoomObj=PersonalChatRoom.objects.get(RoomName=RoomName)
        RoomObj.members_online.remove(user)
        
    async def disconnect(self,close_code):
        await database_sync_to_async(self.offline_members)(self.RoomObjName,self.scope['user'])        
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    def get_user(self):
        return User.objects.get(username=self.user)
    
    def get_chat_partner(self):
        return User.objects.get(username=self.chat_partner)
    
    def create_chat_object(self,user,chat_partner,message):
        ChatObj=PersonalChat.objects.create(chat=message,sender=user,reciever=chat_partner)
        for i in self.RoomObj.members_online.all():            
            ChatObj.viewed_by.add(i)
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.user=text_data_json['user']
        self.chat_partner=text_data_json['chat_partner']
        self.user_obj = await database_sync_to_async(self.get_user)()
        self.chat_partner_obj = await database_sync_to_async(self.get_chat_partner)()
        self.message = text_data_json['message']
        # Send message to room group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'sender':self.user,
                'reciever':self.chat_partner,
                'message': self.message
            }
        )
        await database_sync_to_async(self.create_chat_object)(self.user_obj,self.chat_partner_obj,self.message)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender':event['sender'],
            'reciever':event['reciever']
        }))      
    
    @receiver(m2m_changed,sender=PersonalChatRoom.chats.through)
    def m2m_changed_reciever(instance,pk_set,action,sender,*args,**kwargs):              
        if action == 'post_add':
            for i in instance.chats.all():
                i.viewed_by.add(i.sender) 
            
            
class NotificationConsumer(AsyncWebsocketConsumer):
        
    async def connect(self):   
        await self.accept()       
        self.user=self.scope['user']
        await database_sync_to_async(self.online_user)()         
        NotificationConsumer.group_name=f'{self.scope["url_route"]["kwargs"]["userforgroup"]}_notify'        
        await self.channel_layer.group_add(
            NotificationConsumer.group_name,
            self.channel_name
        )        
        
    def online_user(self):
        self.user.first_name='Online'
        self.user.save()
        
    def offline_user(self):
        now=datetime.datetime.now()
        time=now.strftime("%H:%M")
        self.user.first_name=str(time)
        self.user.save()
        
    async def disconnect(self,close_code):
        await database_sync_to_async(self.offline_user)()       
    
    async def personal_notifications(self,event):
        await self.send(
            json.dumps({
                'type':'Personal Notification',
                'reciever_id':event['reciever_id'],
                'reciever_username':event['reciever_username'],
                'sender_id':event['sender_id'],
                'sender_username':event['sender_username'],
                'chat':event['chat'],
                'counter':event['counter'],
            })
        )
        
    async def group_notifications(self,event):
        await self.send(
            json.dumps({
                'type':'Group Notification',
                'chat':event['chat'],
                'counter':event['counter'],
                'groupid':event['groupid'],
            })
        )
       

@receiver(m2m_changed,sender=PersonalChatRoom.chats.through)
def NotificationSend(instance,pk_set,action,sender,*args,**kwargs):
    if action == 'post_add':
        chat_obj=instance.chats.last()
        sender_=chat_obj.sender
        reciever=chat_obj.reciever
        instance.last_updated=datetime.datetime.now()
        instance.save()
        reciever_for_group=remove_unnecessary(reciever.username)
        if reciever not in instance.members_online.all() and reciever not in chat_obj.viewed_by.all():
            counter=1
            channel_layer=get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'{reciever_for_group}_notify',{
                    'type':'personal_notifications',
                    'reciever_id':reciever.id,
                    'reciever_username':reciever.username,
                    'sender_id':sender_.id,
                    'sender_username':sender_.username,
                    'chat':chat_obj.chat,
                    'counter':counter
                }
            )
    
        
@receiver(m2m_changed,sender=GroupChatRoom.chats.through)
def group_message_update(sender,instance,action,*args,**kwargs):
    if action == 'post_add':
        chat_obj=instance.chats.last()
        sender_=chat_obj.sender
        reciever=chat_obj.reciever.all()    
        instance.last_updated=datetime.datetime.now()
        instance.save()    
        for i in reciever:
            if i not in instance.members_online.all() and i not in chat_obj.viewed_by.all():                
                reciever_for_group=remove_unnecessary(i.username)
                counter=1
                channel_layer=get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f'{reciever_for_group}_notify',{
                        'type':'group_notifications',                        
                        'chat':chat_obj.chat,
                        'counter':counter,
                        'groupid':instance.id,
                    }
                )
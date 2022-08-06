import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from chats.models import PersonalChat,PersonalChatRoom
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
import datetime

class OnlineUserConsumer(AsyncWebsocketConsumer):
    async def connect(self):     
        await self.accept()  
        self.user=self.scope['user']
        await database_sync_to_async(self.online_user)()
        print(self.user.first_name)
        
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
        print(self.user.first_name)
        print(f'last scene is:{self.user.last_name}')
    
                    
        
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
        print(self.group_name)
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
        await database_sync_to_async(self.create_chat_object)(self.user_obj,self.chat_partner_obj,self.message)

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
        print(pk_set)                            
        for i in instance.chats.all():
            i.viewed_by.add(i.sender) 
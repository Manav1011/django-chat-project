import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from groups.models import GroupChatRoom,GroupChat
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User



class GroupChatConsumer(AsyncWebsocketConsumer):
    def onlineusers(self,RoomId,user):
        qs=GroupChatRoom.objects.get(id=RoomId)
        qs.members_online.add(user)    
        
    async def connect(self):
        self.group_name=f"GroupChatRoom_{self.scope['url_route']['kwargs']['RoomName']}"
        self.user=self.scope['user']
        self.room_id=self.scope['url_route']['kwargs']['RoomId']
        await database_sync_to_async(self.onlineusers)(self.room_id,self.user)
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        
        
        
    def OfflineUsers(self,RoomId,user):        
        RoomObj=GroupChatRoom.objects.get(id=RoomId)        
        RoomObj.members_online.remove(user)
            
        
        
    async def disconnect(self, code):        
        await database_sync_to_async(self.OfflineUsers)(self.scope['url_route']['kwargs']['RoomId'],self.user)
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    
    async def GroupRoomChatSend(self,event):          
        await self.send(text_data=json.dumps({
            'message':event['message'],
            'sender':event['sender'],
        }))
    
    def get_room_obj(self,RoomId):
        return GroupChatRoom.objects.get(id=RoomId)
    
    def create_messages(self,RoomId,message,sender):
        RoomObj=GroupChatRoom.objects.get(id=RoomId)
        userobj=User.objects.get(username=sender)
        chat_obj=GroupChat.objects.create(chat=message,sender=userobj)
        for i in RoomObj.members_online.all():
            chat_obj.viewed_by.add(i)
        for i in RoomObj.members.all():
            chat_obj.reciever.add(i)
        RoomObj.chats.add(chat_obj)

    async def receive(self,text_data):
        json_text_data=json.loads(text_data)
        print(json_text_data)
        self.RoomId=json_text_data['GroupRoomId']
        self.sender=json_text_data['sender']
        message=json_text_data['message']        
        self.GroupRoomObj=database_sync_to_async(self.get_room_obj)(self.RoomId)
        print(self.GroupRoomObj)
        await database_sync_to_async(self.create_messages)(self.RoomId,message,self.sender)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type':'GroupRoomChatSend',
                'message':message,
                'sender':self.sender,
            }
        )        
        

    
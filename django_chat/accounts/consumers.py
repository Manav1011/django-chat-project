import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from chats.models import PersonalChat,PersonalChatRoom
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class MessageNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):     
        await self.accept()  
        MessageNotificationConsumer.user=self.scope['user']
        MessageNotificationConsumer.group_name=f'chat_notifcation_{MessageNotificationConsumer.user.username}'
        await self.channel_layer.group_add(
            MessageNotificationConsumer.group_name,
            self.channel_name
        )        
        
    async def disconnect(self,close_code):
        pass
    
    async def chat_notification(self,event):
        await self.send(
            json.dumps({
                'type':'chat_notify',
                'count':event['count'],
                'partner_id':event['partner_id'],
                'chat':event['chat']
            })
        )
    
    @receiver(m2m_changed,sender=PersonalChatRoom.chats.through)
    def m2m_changed_reciever(instance,action,sender,*args,**kwargs):
        print(action)
        if MessageNotificationConsumer.user in instance.members.all():
            count=0
            room_partners={}
            for i in instance.members.all().exclude(username=MessageNotificationConsumer.user.username):
                room_partners.update({i:i})
            partner_id=None
            for i in room_partners:
                partner_id=i.id
            for i in instance.chats.all():
                if i.is_viewed == False:
                    count+=1
        channel_layer=get_channel_layer()                         
        async_to_sync(channel_layer.group_send)(
            MessageNotificationConsumer.group_name,           
            {
                'type':'chat_notification',
                'count':count,
                'partner_id':partner_id,
                'chat':str(instance.chats.last())
            }
        )
                    
        
    
    
    # async def chat_notification(self,event):
    #     await self.send(
    #         json.dumps({
    #             'type':event['created'],
    #             'reciever':event['reciever'],
    #             'sender':event['sender'],
    #             'chat':event['chat']
    #         })
    #     )
    
    # @receiver(post_save,sender=PersonalChat)
    # def get_perssonal_chats(instance,created,*args,**kwargs):
    #     channel_layer=get_channel_layer()     
    #     print(instance.reciever.username)   
    #     print(instance.chat)
        # async_to_sync(channel_layer.group_send)(
        #     MessageNotificationConsumer.group_name,           
        #     {
        #         'type':'chat_notification',
        #         'reciever':instance.reciever.username,
        #         'sender':instance.sender.username,
        #         'created':created,
        #         'chat':instance.chat
        #     }
        # )
        
    # async def delete_chat_notification(self,event):
    #     await self.send(
    #         json.dumps({
    #             'type':'deleted',
    #             'reciever':event['reciever'],
    #             'chat':event['chat']
    #         })
    #     )
    # @receiver(post_delete,sender=PersonalChat)
    # def on_delete_perssonal_chats(instance,*args,**kwargs):
    #     channel_layer=get_channel_layer()             
    #     chat_objects=PersonalChat.objects.get_personal_chats(instance.sender)
    #     async_to_sync(channel_layer.group_send)(
    #         MessageNotificationConsumer.group_name,           
    #         {
    #             'type':'delete_chat_notification',
    #             'reciever':instance.reciever.username,
            
    #         }
    #     )
        
    
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import async_to_sync
# from django.dispatch import receiver
# from django.db.models.signals import post_save,post_delete
# from chats.models import PersonalChat
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer

# class MessageNotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         MessageNotificationConsumer.user=self.scope["user"]
#         MessageNotificationConsumer.group_name=f'notify_{self.scope["user"]}'
#         self.group_name=f'notify_{self.scope["user"]}'
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         await self.accept()
        
#     async def disconnect(self,close_code):
#         pass
    
#     async def chat_notification(self,event):
#         await self.send(
#             json.dumps({
#                 'type':event['created'],
#                 'reciever':event['reciever'],
#                 'sender':event['sender'],
#                 'chat':event['chat']
#             })
#         )
    
#     @receiver(post_save,sender=PersonalChat)
#     def get_perssonal_chats(instance,created,*args,**kwargs):
#         channel_layer=get_channel_layer()     
#         print(instance.reciever.username)   
#         print(instance.chat)
#         async_to_sync(channel_layer.group_send)(
#             MessageNotificationConsumer.group_name,           
#             {
#                 'type':'chat_notification',
#                 'reciever':instance.reciever.username,
#                 'sender':instance.sender.username,
#                 'created':created,
#                 'chat':instance.chat
#             }
#         )
        
#     async def delete_chat_notification(self,event):
#         await self.send(
#             json.dumps({
#                 'type':'deleted',
#                 'reciever':event['reciever'],
#                 'chat':event['chat']
#             })
#         )
#     @receiver(post_delete,sender=PersonalChat)
#     def on_delete_perssonal_chats(instance,*args,**kwargs):
#         channel_layer=get_channel_layer()             
#         chat_objects=PersonalChat.objects.get_personal_chats(instance.sender)
#         async_to_sync(channel_layer.group_send)(
#             MessageNotificationConsumer.group_name,           
#             {
#                 'type':'delete_chat_notification',
#                 'reciever':instance.reciever.username,
            
#             }
#         )
        
    
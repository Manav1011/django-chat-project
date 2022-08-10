from django.urls import path
from .consumers import PersonalChatConsumer,NotificationConsumer
from groups.consumers import GroupChatConsumer

websocket_urlpatterns=[    
    path('ws/<str:userforgroup>/<str:user>/notify/',NotificationConsumer.as_asgi()),
    path('ws/chat/<str:RoomObjName>/<str:RoomName>/',PersonalChatConsumer.as_asgi()),
    path('ws/group_chat/<int:RoomId>/<str:RoomName>/',GroupChatConsumer.as_asgi()),
]
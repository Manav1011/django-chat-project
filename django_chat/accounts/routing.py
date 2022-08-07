from django.urls import path
from .consumers import PersonalChatConsumer,NotificationConsumer

websocket_urlpatterns=[    
    path('ws/<str:userforgroup>/<str:user>/notify/',NotificationConsumer.as_asgi()),
    path('ws/chat/<str:RoomObjName>/<str:RoomName>/',PersonalChatConsumer.as_asgi()),
]
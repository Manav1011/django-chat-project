from django.urls import path
from .consumers import MessageNotificationConsumer,PersonalChatConsumer

websocket_urlpatterns=[
    path('ws/<str:user>/notify/',MessageNotificationConsumer.as_asgi()),
    path('ws/chat/<str:RoomName>/',PersonalChatConsumer.as_asgi()),
]
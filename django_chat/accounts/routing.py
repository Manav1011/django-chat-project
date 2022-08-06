from django.urls import path
from .consumers import OnlineUserConsumer,PersonalChatConsumer

websocket_urlpatterns=[
    path('ws/notify/',OnlineUserConsumer.as_asgi()),
    path('ws/chat/<str:RoomObjName>/<str:RoomName>/',PersonalChatConsumer.as_asgi()),
]
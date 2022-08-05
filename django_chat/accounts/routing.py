from django.urls import path
from .consumers import MessageNotificationConsumer

websocket_urlpatterns=[
    path('ws/<str:user>/notify/',MessageNotificationConsumer.as_asgi())
]
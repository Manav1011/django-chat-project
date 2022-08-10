from django.urls import path,re_path
from .views import group_chat_room

app_name='groups'

urlpatterns=[
    path('GroupChatRoom/<int:pk>/',group_chat_room,name='group_chat_room')
    ]
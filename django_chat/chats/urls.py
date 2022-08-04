from django.urls import path,re_path
from .views import create_personal_room
app_name='chats'
 
urlpatterns=[
    path('ChatRoom/<int:pk>',create_personal_room,name='create_personal_room'),
    # re_path(r'^PersonalChatRoom/$',show_personal_chat_room,name='personal_chat_room'),
]
from django.urls import path,re_path
from .views import create_personal_room
app_name='chats'
 
urlpatterns=[
    re_path(r'ChatRoom/',create_personal_room,name='create_personal_room')
]
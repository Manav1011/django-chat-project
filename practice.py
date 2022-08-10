from django.contrib.auth.models import User
from chats.models import PersonalChat,PersonalChatRoom

chat_roomobj=PersonalChat.objects.first()
print(chat_roomobj)
for i in chat_roomobj:
    if user1 in i.members.all() and user2 in i.members.all():
        new_obj=i
        print('True')
        
    else:
        print('False')
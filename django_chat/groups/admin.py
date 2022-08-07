from django.contrib import admin
from .models import GroupChatRoom,GroupChat

# Register your models here.

admin.site.register(GroupChat)
admin.site.register(GroupChatRoom)
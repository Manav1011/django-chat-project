from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PersonalChatManager(models.Manager):
    def get_personal_chats(self,user):
        chat_objects=self.get_queryset().filter(sender=user).values('reciever').distinct()
        qs={}
        for i in chat_objects:
            qs.update({f'object {i["reciever"]}':PersonalChat.objects.filter(reciever=i['reciever']).all().last()})    
        return qs

class PersonalChat(models.Model):
    chat=models.CharField(max_length=500,null=False,blank=False)
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    reciever=models.ForeignKey(User,related_name='reciever',on_delete=models.CASCADE,null=False,blank=False)
    timestamp=models.DateTimeField(auto_now_add=True)   
    
    def __str__(self):
        return f'sender: {self.sender} reciever: {self.reciever}'
    
    objects=PersonalChatManager()



from .models import GroupChatRoom
from django import forms

class NewGroupForm(forms.ModelForm):
    class Meta:
        model=GroupChatRoom
        fields=('RoomName','members')
    
from django import forms
from .models import Message

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['reply']  

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['full_name', 'email', 'message']

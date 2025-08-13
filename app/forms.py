from django import forms
from .models import Message

class ReplyForm(forms.Form):
    class Meta:
        model = Message
        fields = ['reply']  

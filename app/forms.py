from django import forms
from .models import Message

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['reply']  

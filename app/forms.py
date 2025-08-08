from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model= ContactMessage
        fields = ['full_name', 'email', 'message']

class ReplyForm(forms.Form):
    reply = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), label="Your Reply")
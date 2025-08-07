from django.db import models



# Create your models here.
class ContactMessage(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    replied = models.BooleanField(default=False)
    viewed = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __srt__(self):
        return f"Message from {self.full_name}" 
    

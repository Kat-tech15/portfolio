from django.db import models



# Create your models here.
class Message(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    STATUS_CHOICES  = [
        ('new', 'New'),
        ('viewed', 'Viewed'),
        ('replied', 'Replied'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.message}" 
    

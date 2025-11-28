from django.db import models



# Create your models here.
class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    STATUS_CHOICES  = [
        ('new', 'New'),
        ('viewed', 'Viewed'),
        ('replied', 'Replied'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    response = models.TextField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.message}" 
    

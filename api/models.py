from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(blank=True, upload_to='profile_pic', default='default.jpg')
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["created"]
        
    def __str__(self):
        return self.user
    
    
class PDFModel(models.Model):
    title = models.TextField(blank=False, null=False)
    image = models.URLField(blank=False, null=False)
    download = models.URLField(blank=False, null=False)
    size = models.TextField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title
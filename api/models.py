from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

SEMESTER_CHOICES = [
    ('first', 'FIRST'),
    ('second', 'SECOND')
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(blank=True, upload_to='profile_pic', default='default.jpg')
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created"]
        
    def __str__(self):
        return f'{self.user}'
    
class FolderModel(models.Model):
    file = models.CharField(max_length=20)
    level = models.CharField(max_length=20)
    semester = models.CharField(max_length=50, choices=SEMESTER_CHOICES, default="first")
    
    def __str__(self):
        return self.file
 
class PDFModel(models.Model):
    file = models.ForeignKey(FolderModel, on_delete=models.CASCADE, related_name='pdf_file')
    title = models.CharField(max_length=100)
    image = models.URLField(blank=False)
    download = models.URLField(blank=False)
    size = models.CharField(max_length=10, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title
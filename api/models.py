from django.db import models

# Create your models here.

SEMESTER_CHOICES = [
    ('first', 'FIRST'),
    ('second', 'SECOND')
]
    
class FolderModel(models.Model):
    category = models.CharField(max_length=20)
    level = models.CharField(max_length=20)
    semester = models.CharField(max_length=50, choices=SEMESTER_CHOICES, default="first")
    
    class Meta:
        ordering = ['category']
        
    def __str__(self):
        return self.category
 
class PDFModel(models.Model):
    category = models.ForeignKey(FolderModel, on_delete=models.CASCADE, related_name='pdf_file')
    title = models.CharField(max_length=100)
    image = models.URLField(blank=False)
    download = models.URLField(blank=False)
    size = models.CharField(max_length=10, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title
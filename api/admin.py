from django.contrib import admin
from .models import Profile, PDFModel, FolderModel

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image']
    list_filter = ['created']
    search_fields = ['user.email']
  
  
class PDFModelAdminInline(admin.StackedInline):
    model = PDFModel
    raw_id_fields = ['file']
    
    
@admin.register(FolderModel)
class FolderModelAdmin(admin.ModelAdmin):
    list_display = ['file', 'level', 'semester']
    list_filter = ['level', 'semester']
    inlines = [PDFModelAdminInline]
    
from django.contrib import admin
from .models import PDFModel, FolderModel

# Register your models here.
  
class PDFModelAdminInline(admin.StackedInline):
    model = PDFModel
    readonly_field = ['category']
    
    
@admin.register(FolderModel)
class FolderModelAdmin(admin.ModelAdmin):
    list_display = ['category', 'level', 'semester']
    list_filter = ['level', 'semester']
    inlines = [PDFModelAdminInline]
    
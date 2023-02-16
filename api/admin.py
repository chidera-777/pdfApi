from django.contrib import admin
from .models import Profile, PDFModel

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image']
    list_filter = ['user', 'image', 'created']
    search_fields = ['user.email']
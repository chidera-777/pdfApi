from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from django.contrib.auth import get_user_model
import csv, datetime

# Register your models here.
User = get_user_model()

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;' 'filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'  #short description
    
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
          'classes': ['wide'],
          'fields': ('email', 'password')
        }),
        (('Personal_info'), {
          'classes': ['wide'],
          'fields': ('first_name', 'last_name')
        }),
        (('Permissions'), {
          'classes': ['wide'],
          'fields': ('is_superuser', 'is_staff', 'is_active', 'groups')
        }),
    )
    add_fieldsets = (
        (None, {
          'classes': ('wide',),
          'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')}
        ),
    )  
    list_display = ['email', 'first_name', 'is_staff']
    list_filter = ['email', 'is_staff', 'is_active']
    search_fields = ['email']
    ordering = ('email',)  
    actions = [export_to_csv] 

admin.site.register(get_user_model(), CustomUserAdmin)  


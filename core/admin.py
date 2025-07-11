from django.contrib import admin
from .models import Registration

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'email', 'phone', 'job_title', 'company_name',
        'company_address', 'state', 'zip_code'
    )
    search_fields = ('first_name', 'last_name', 'email', 'company_name')
    list_filter = ('state',)

admin.site.site_header = "USATA Admin Panel"
admin.site.site_title = "USATA Admin"
admin.site.index_title = "Welcome to the USATA Dashboard"
from django.contrib import admin
from .models import Registration
from django.urls import path
from django.http import HttpResponseRedirect

# 1. First define your custom admin site
class USATAAdminSite(admin.AdminSite):
    site_header = "USATA Admin Panel"
    site_title = "USATA Admin"
    index_title = "Welcome to the USATA Dashboard"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('r/', lambda request: HttpResponseRedirect('https://usata.co'), name='view_site'),
        ]
        return custom_urls + urls

# 2. Then instantiate it
admin_site = USATAAdminSite(name='usata_admin')

# 3. Now register models using your custom admin site
@admin.register(Registration, site=admin_site)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'email', 'phone', 'job_title', 'company_name',
        'company_address', 'state', 'zip_code'
    )
    search_fields = ('first_name', 'last_name', 'email', 'company_name')
    list_filter = ('state',)

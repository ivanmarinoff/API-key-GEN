from django.contrib import admin

from .models import APIKey


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'created_at', 'expires_at', 'is_valid', 'site_url')
    list_filter = ('created_at', 'expires_at', 'site_url')
    search_fields = ('site_url',)


admin.site.site_header = 'API Key Generator'
admin.site.site_title = 'API Key Generator'



from django.contrib import admin
from .models import APIKey


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'created_at', 'expires_at', 'is_valid', 'site_url')
    list_filter = ('created_at', 'expires_at', 'site_url')
    search_fields = ('site_url',)
    fields = ('site_url', 'key', 'created_at', 'expires_at', 'validity_duration', 'auto_set_expiration')
    readonly_fields = ('created_at', 'key')  # Make `created_at` and `key` read-only to prevent edits


# Customize admin panel appearance
admin.site.site_header = 'API Key Generator'
admin.site.site_title = 'API Key Generator'

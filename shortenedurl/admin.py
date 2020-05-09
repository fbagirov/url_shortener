from django.contrib import admin
from .models import URL


@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    readonly_fields = ('shortened_url', 'hits', 'created_at')
    list_display = ('shortened_url', 'full_url', 'hits', 'created_at')
    list_display_links = ('shortened_url',)

from django.contrib import admin
from .models import URL, Access, ClickedDistribution


@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    readonly_fields = ('shortened_url', 'hits', 'created_at')
    list_display = ('shortened_url', 'full_url', 'hits', 'created_at')
    list_display_links = ('shortened_url',)


@admin.register(Access)
class AccessAdmin(admin.ModelAdmin):
    list_display = ('url', 'user', 'hits',)
    list_display_links = ('url',)
    readonly_fields = ('hits',)


@admin.register(ClickedDistribution)
class ClickedDistributionAdmin(admin.ModelAdmin):
    list_display = ('url', 'user', 'clicked_at',)
    list_display_links = ('url',)

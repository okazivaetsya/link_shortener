from django.contrib import admin

from .models import Tokens


@admin.register(Tokens)
class TokenAdmin(admin.ModelAdmin):
    """Настройки админки для модели Токенов"""
    list_display = (
        'full_url',
        'short_url',
        'requests_count',
        'created_date',
        'is_active'
    )
    search_fields = ('full_url', 'short_url')
    ordering = ('-created_date',)

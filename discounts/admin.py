from django.contrib import admin
from .models import Discount


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'hotel',
        'discount_type',
        'value',
        'valid_from',
        'valid_until',
        'usage_limit',
        'used_count',
        'is_active',
    )

    list_filter = (
        'discount_type',
        'is_active',
        'hotel',
    )

    search_fields = ('code', 'hotel__name')

    readonly_fields = ('created_at',)

    ordering = ('-created_at',)
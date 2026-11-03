from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'hotel',
        'rating',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'rating',
        'created_at',
        'hotel',
    )

    search_fields = (
        'user__username',
        'user__email',
        'hotel__name',
        'comment',
    )

    readonly_fields = ('created_at', 'updated_at')

    ordering = ('-created_at',)
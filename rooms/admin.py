from django.contrib import admin
from .models import RoomType


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'hotel',
        'capacity',
        'price_per_night',
        'quantity',
        'created_at',
    )

    list_filter = ('hotel', 'capacity')

    search_fields = ('title', 'hotel__name')

    ordering = ('hotel', 'title')
from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'room_type',
        'check_in',
        'check_out',
        'guests',
        'rooms_count',
        'total_price',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'check_in',
        'check_out',
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__email',
        'room_type__title',
        'room_type__hotel__name',
    )

    readonly_fields = ('created_at', 'updated_at')

    ordering = ('-created_at',)
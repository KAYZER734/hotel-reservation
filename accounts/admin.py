from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, HotelAdminRequest


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
    )

    search_fields = ('username', 'email', 'first_name', 'last_name')

    list_filter = ('is_staff', 'is_active', 'is_superuser')


@admin.register(HotelAdminRequest)
class HotelAdminRequestPanel(admin.ModelAdmin):
    list_display = (
        'user',
        'hotel',
        'status',
        'created_at',
        'reviewed_by',
    )

    list_filter = ('status', 'created_at')

    search_fields = (
        'user__username',
        'user__email',
        'hotel__name',
    )

    readonly_fields = ('created_at',)
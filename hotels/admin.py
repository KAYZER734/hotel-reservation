from django.contrib import admin
from .models import Hotel, HotelAdmin, HotelRegistrationRequest


@admin.register(Hotel)
class HotelAdminPanel(admin.ModelAdmin):
    list_display = ('name', 'city', 'created_at')
    search_fields = ('name', 'city')
    list_filter = ('city',)


@admin.register(HotelAdmin)
class HotelAdminAssignmentPanel(admin.ModelAdmin):
    list_display = ('user', 'hotel', 'is_active', 'assigned_at')
    list_filter = ('is_active', 'hotel')
    search_fields = ('user__username', 'hotel__name')


@admin.register(HotelRegistrationRequest)
class HotelRegistrationRequestPanel(admin.ModelAdmin):
    list_display = ('name', 'city', 'submitted_by', 'status', 'created_at')
    list_filter = ('status', 'city')
    search_fields = ('name', 'city', 'submitted_by__username')

from django.contrib import admin
from django.utils import timezone

from .models import Hotel, HotelAdmin, HotelRegistrationRequest


# تأیید درخواست ثبت هتل
@admin.action(description='تأیید درخواست و ایجاد هتل')
def approve_hotel_requests(modeladmin, request, queryset):

    for request_obj in queryset.filter(
        status=HotelRegistrationRequest.Status.PENDING
    ):

        # ایجاد هتل
        hotel = Hotel.objects.create(
            name=request_obj.name,
            city=request_obj.city,
            address=request_obj.address,
            description=request_obj.description
        )

        # ثبت درخواست دهنده به عنوان مدیر هتل
        HotelAdmin.objects.get_or_create(
            user=request_obj.submitted_by,
            hotel=hotel,
            defaults={'is_active': True}
        )

        # تغییر وضعیت درخواست
        request_obj.status = HotelRegistrationRequest.Status.APPROVED
        request_obj.reviewed_at = timezone.now()
        request_obj.reviewed_by = request.user

        request_obj.save()


# رد درخواست ثبت هتل
@admin.action(description='رد درخواست')
def reject_hotel_requests(modeladmin, request, queryset):

    queryset.filter(
        status=HotelRegistrationRequest.Status.PENDING
    ).update(
        status=HotelRegistrationRequest.Status.REJECTED,
        reviewed_at=timezone.now(),
        reviewed_by=request.user
    )


# مدیریت درخواست های ثبت هتل
@admin.register(HotelRegistrationRequest)
class HotelRegistrationRequestAdmin(admin.ModelAdmin):

    list_display = [
        'name',
        'city',
        'submitted_by',
        'status',
        'created_at',
    ]

    list_filter = [
        'status',
        'city',
    ]

    actions = [
        approve_hotel_requests,
        reject_hotel_requests,
    ]


# مدیریت هتل ها
@admin.register(Hotel)
class HotelAdminPanel(admin.ModelAdmin):

    list_display = [
        'name',
        'city',
        'created_at',
    ]


# مدیریت مدیران هتل
@admin.register(HotelAdmin)
class HotelAdminManagement(admin.ModelAdmin):

    list_display = [
        'user',
        'hotel',
        'is_active',
        'assigned_at',
    ]

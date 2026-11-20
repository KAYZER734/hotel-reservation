
from django.urls import path

from .views import (
    BookingCreateView,
    MyBookingListView,
    BookingDetailView,
    BookingCancelView,
    ManagerBookingListView,
    ManagerBookingStatusUpdateView,
)

app_name = 'bookings'

urlpatterns = [

    # ثبت رزرو
    path( 'create/<int:room_type_pk>/', BookingCreateView.as_view(), name='booking_create' ),

    # رزروهای کاربر
    path( 'my/', MyBookingListView.as_view(), name='my_bookings' ),

    # جزئیات رزرو
    path( 'my/<int:pk>/', BookingDetailView.as_view(), name='booking_detail' ),

    # لغو رزرو
    path( 'my/<int:pk>/cancel/', BookingCancelView.as_view(), name='booking_cancel' ),

    # رزروهای مدیر هتل
    path( 'hotel/<int:hotel_pk>/', ManagerBookingListView.as_view(), name='manager_bookings' ),

    # تغییر وضعیت رزرو
    path( 'hotel/<int:hotel_pk>/<int:pk>/status/', ManagerBookingStatusUpdateView.as_view(), name='booking_status_update' ),

]

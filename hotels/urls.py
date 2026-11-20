
from django.urls import path

from .views import (
    HotelListView,
    HotelDetailView,
    HotelRequestCreateView,
    MyHotelRequestsView,
    AdminHotelRequestsView,
    HotelRequestReviewView,
    MyHotelsView
)


app_name = 'hotels'


urlpatterns = [

    # مشاهده هتل ها
    path('', HotelListView.as_view(), name='hotel_list'),
    path( '<int:pk>/', HotelDetailView.as_view(), name='hotel_detail' ),

    # ثبت درخواست هتل
    path( 'request/', HotelRequestCreateView.as_view(), name='hotel_request' ),

    # درخواست های کاربر
    path( 'my-requests/', MyHotelRequestsView.as_view(), name='my_hotel_requests' ),

    # هتل های تحت مدیریت کاربر
    path( 'my-hotels/', MyHotelsView.as_view(), name='my_hotels' ),

    # مدیریت درخواست ها توسط مدیر کل
    path( 'admin/requests/', AdminHotelRequestsView.as_view(), name='admin_hotel_requests' ),
    path( 'admin/requests/<int:pk>/review/', HotelRequestReviewView.as_view(), name='review_hotel_request' ),

]

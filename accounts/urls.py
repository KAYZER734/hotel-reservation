
from django.urls import path

from .views import (
    RegisterView,
    UserLoginView,
    UserLogoutView,
    ProfileView,
    ProfileUpdateView,
    HotelAdminRequestCreateView,
    MyHotelAdminRequestsView,
    AdminHotelAdminRequestsView,
    HotelAdminRequestReviewView
)


app_name = 'accounts'

urlpatterns = [

    # ثبت نام و ورود و خروج
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # پروفایل
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),

    # درخواست مدیریت هتل
    path( 'hotel-admin/request/', HotelAdminRequestCreateView.as_view(), name='hotel_admin_request' ),

    path( 'my-requests/', MyHotelAdminRequestsView.as_view(), name='my_requests' ),

    # مدیریت درخواست ها توسط مدیر کل
    path( 'admin/requests/', AdminHotelAdminRequestsView.as_view(), name='admin_requests' ),

    path( 'admin/requests/<int:pk>/review/', HotelAdminRequestReviewView.as_view(), name='review_request' ),

]


from django.urls import path

from .views import (
    RoomListView,
    RoomDetailView,
    RoomCreateView,
    RoomUpdateView,
    RoomDeleteView,
    RoomSearchView
)


app_name = 'rooms'


urlpatterns = [

    # نمایش انواع اتاق
    path('', RoomListView.as_view(), name='room_list'),

    # جست وجوی اتاق
    path('search/', RoomSearchView.as_view(), name='room_search'),

    # جزئیات اتاق
    path( '<int:pk>/', RoomDetailView.as_view(), name='room_detail' ),

    # تعریف اتاق برای یک هتل
    path( 'hotel/<int:hotel_pk>/create/', RoomCreateView.as_view(), name='room_create' ),

    # ویرایش اتاق
    path( '<int:pk>/edit/', RoomUpdateView.as_view(), name='room_update' ),

    # حذف اتاق
    path( '<int:pk>/delete/', RoomDeleteView.as_view(), name='room_delete' ),

]


from django.urls import path
from .views import HotelListView, HotelDetailView

app_name = 'hotels'

urlpatterns = [
    path('', HotelListView.as_view(), name='hotel_list'),

    path('<int:pk>/', HotelDetailView.as_view(), name='hotel_detail'),
]



from .views import (
    HotelListView,
    HotelDetailView,
    MyHotelRequestsView,
    HotelRequestDetailView,
    HotelRequestCreateView,
    AdminHotelRequestsView,
    ReviewHotelRequestView,
)

app_name = 'hotels'

urlpatterns = [

    # فهرست هتل‌ها
    path('', HotelListView.as_view(), name='hotel_list'),

    # جزئیات هتل
    path('<int:pk>/', HotelDetailView.as_view(), name='hotel_detail'),

    # درخواست‌های کاربر
    path(
        'my-requests/',
        MyHotelRequestsView.as_view(),
        name='my_requests'
    ),

    # جزئیات درخواست
    path(
        'requests/<int:pk>/',
        HotelRequestDetailView.as_view(),
        name='request_detail'
    ),

    # مدیریت درخواست‌ها توسط مدیر کل
    path(
        'admin/requests/',
        AdminHotelRequestsView.as_view(),
        name='admin_requests'
    ),

    # تأیید یا رد درخواست
    path(
        'admin/requests/<int:pk>/review/',
        ReviewHotelRequestView.as_view(),
        name='review_request'
    ),
]


from django.urls import path

from .views import (
    HotelListView,
    HotelDetailView,
    HotelRequestCreateView,
    MyHotelRequestsView,
    HotelRequestDetailView,
    MyManagedHotelsView,
    HotelUpdateView,
    HotelDeleteView,
    HotelAdminListView,
    HotelAdminCreateView,
    HotelAdminDeleteView,
)

app_name = 'hotels'

urlpatterns = [
    path('', HotelListView.as_view(), name='hotel_list'),

    path(
        'request/create/',
        HotelRequestCreateView.as_view(),
        name='hotel_request_create'
    ),

    path(
        'my-requests/',
        MyHotelRequestsView.as_view(),
        name='my_requests'
    ),

    path(
        'requests/<int:pk>/',
        HotelRequestDetailView.as_view(),
        name='request_detail'
    ),

    path(
        '<int:pk>/',
        HotelDetailView.as_view(),
        name='hotel_detail'
    ),

    path(
        'my-managed-hotels/',
        MyManagedHotelsView.as_view(),
        name='my_managed_hotels'
    ),

    path(
        '<int:pk>/edit/',
        HotelUpdateView.as_view(),
        name='hotel_update'
    ),

    path(
        '<int:pk>/',
        HotelDetailView.as_view(),
        name='hotel_detail'
    ),

    path(
        '<int:pk>/delete/',
        HotelDeleteView.as_view(),
        name='hotel_delete'
    ),

    path(
        '<int:pk>/administrators/',
        HotelAdminListView.as_view(),
        name='hotel_admins'
    ),

    path(
        '<int:pk>/administrators/add/',
        HotelAdminCreateView.as_view(),
        name='hotel_admin_add'
    ),

    path(
        '<int:pk>/administrators/<int:admin_pk>/delete/',
        HotelAdminDeleteView.as_view(),
        name='hotel_admin_delete'
    ),
]

from .views import MyManagedHotelsView

path(
    'my-managed-hotels/',
    MyManagedHotelsView.as_view(),
    name='my_managed_hotels'
),
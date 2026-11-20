
from django.urls import path
from . import views

app_name = 'discounts'

urlpatterns = [

    # نمایش کدهای تخفیف هتل
    path( 'hotel/<int:hotel_pk>/', views.DiscountListView.as_view(), name='discount_list' ),

    # ایجاد کد تخفیف
    path( 'hotel/<int:hotel_pk>/create/', views.DiscountCreateView.as_view(), name='discount_create' ),

    # ویرایش کد تخفیف
    path( 'hotel/<int:hotel_pk>/<int:pk>/edit/', views.DiscountUpdateView.as_view(), name='discount_update' ),

    # حذف کد تخفیف
    path( 'hotel/<int:hotel_pk>/<int:pk>/delete/', views.DiscountDeleteView.as_view(), name='discount_delete' ),

]

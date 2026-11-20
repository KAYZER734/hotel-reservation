
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [

    path( 'hotel/<int:hotel_pk>/', views.ReviewListView.as_view(), name='review_list' ),

    path( 'hotel/<int:hotel_pk>/create/', views.ReviewCreateView.as_view(), name='review_create' ),

    path( 'my/<int:pk>/edit/', views.ReviewUpdateView.as_view(), name='review_update' ),

    path( 'my/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review_delete' ),

]

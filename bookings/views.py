
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    View,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages

from hotels.models import HotelAdmin
from rooms.models import RoomType

from .models import Booking
from .forms import BookingForm, BookingStatusForm


# ثبت رزرو توسط کاربر
class BookingCreateView(LoginRequiredMixin, CreateView):

    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_create.html'
    success_url = reverse_lazy('bookings:my_bookings')

    def dispatch(self, request, *args, **kwargs):
        self.room_type = get_object_or_404(
            RoomType,
            pk=kwargs['room_type_pk']
        )
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['room_type'] = self.room_type
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_type'] = self.room_type
        return context

    def form_valid(self, form):

        booking = form.save(commit=False)

        booking.user = self.request.user
        booking.room_type = self.room_type

        # محاسبه تعداد شب‌ها
        nights = (
            booking.check_out - booking.check_in
        ).days

        # محاسبه مبلغ کل
        booking.total_price = (
            self.room_type.price_per_night
            * nights
            * booking.rooms_count
        )

        booking.save()

        messages.success(
            self.request,
            'رزرو شما با موفقیت ثبت شد.'
        )

        return redirect(self.success_url)


# مشاهده رزروهای کاربر
class MyBookingListView(LoginRequiredMixin, ListView):

    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(
            user=self.request.user
        )


# مشاهده جزئیات رزرو
class BookingDetailView(LoginRequiredMixin, DetailView):

    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'

    def get_queryset(self):
        return Booking.objects.filter(
            user=self.request.user
        )


# لغو رزرو توسط کاربر
class BookingCancelView(LoginRequiredMixin, View):

    def post(self, request, pk):

        booking = get_object_or_404(
            Booking,
            pk=pk,
            user=request.user
        )

        if booking.status in [
            Booking.Status.PENDING,
            Booking.Status.CONFIRMED,
        ]:
            booking.status = Booking.Status.CANCELLED
            booking.save()

            messages.success(
                request,
                'رزرو شما لغو شد.'
            )

        return redirect('bookings:my_bookings')


# مشاهده رزروهای هتل توسط مدیر هتل
class ManagerBookingListView(LoginRequiredMixin, ListView):

    model = Booking
    template_name = 'bookings/manager_booking_list.html'
    context_object_name = 'bookings'

    def dispatch(self, request, *args, **kwargs):

        self.hotel_admin = get_object_or_404(
            HotelAdmin,
            user=request.user,
            hotel_id=kwargs['hotel_pk'],
            is_active=True
        )

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):

        return Booking.objects.filter(
            room_type__hotel=self.hotel_admin.hotel
        )


# تغییر وضعیت رزرو توسط مدیر هتل
class ManagerBookingStatusUpdateView(
    LoginRequiredMixin,
    UpdateView
):

    model = Booking
    form_class = BookingStatusForm
    template_name = 'bookings/booking_status_update.html'
    pk_url_kwarg = 'pk'

    def dispatch(self, request, *args, **kwargs):

        self.hotel_admin = get_object_or_404(
            HotelAdmin,
            user=request.user,
            hotel_id=kwargs['hotel_pk'],
            is_active=True
        )

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):

        return Booking.objects.filter(
            room_type__hotel=self.hotel_admin.hotel
        )

    def get_success_url(self):

        return reverse_lazy(
            'bookings:manager_bookings',
            kwargs={'hotel_pk': self.hotel_admin.hotel_id}
        )

    def form_valid(self, form):

        messages.success(
            self.request,
            'وضعیت رزرو با موفقیت تغییر کرد.'
        )

        return super().form_valid(form)

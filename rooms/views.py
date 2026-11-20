
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.http import HttpResponseForbidden

from .models import RoomType
from .forms import RoomTypeForm, RoomSearchForm

from hotels.models import Hotel, HotelAdmin
from bookings.models import Booking


# بررسی مدیر بودن کاربر در یک هتل
class HotelAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):

        hotel_id = self.kwargs.get('hotel_pk')

        if hotel_id:
            return HotelAdmin.objects.filter(
                user=self.request.user,
                hotel_id=hotel_id,
                is_active=True
            ).exists()

        room = self.get_object()

        return HotelAdmin.objects.filter(
            user=self.request.user,
            hotel=room.hotel,
            is_active=True
        ).exists()


# نمایش فهرست انواع اتاق
class RoomListView(ListView):

    model = RoomType

    template_name = 'rooms/room_list.html'

    context_object_name = 'rooms'


# نمایش جزئیات اتاق
class RoomDetailView(DetailView):

    model = RoomType

    template_name = 'rooms/room_detail.html'

    context_object_name = 'room'


# تعریف نوع اتاق توسط مدیر هتل
class RoomCreateView(HotelAdminRequiredMixin, CreateView):

    model = RoomType

    form_class = RoomTypeForm

    template_name = 'rooms/room_form.html'

    def dispatch(self, request, *args, **kwargs):

        self.hotel = get_object_or_404(
            Hotel,
            pk=kwargs['hotel_pk']
        )

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):

        return reverse_lazy(
            'rooms:room_list'
        )

    def form_valid(self, form):

        form.instance.hotel = self.hotel

        return super().form_valid(form)


# ویرایش نوع اتاق
class RoomUpdateView(HotelAdminRequiredMixin, UpdateView):

    model = RoomType

    form_class = RoomTypeForm

    template_name = 'rooms/room_form.html'

    context_object_name = 'room'

    def get_success_url(self):

        return reverse_lazy('rooms:room_detail', kwargs={
            'pk': self.object.pk
        })


# حذف نوع اتاق
class RoomDeleteView(HotelAdminRequiredMixin, DeleteView):

    model = RoomType

    template_name = 'rooms/room_confirm_delete.html'

    success_url = reverse_lazy('rooms:room_list')


# جست وجوی اتاق

from datetime import timedelta

# جست وجوی اتاق
class RoomSearchView(ListView):

    model = RoomType
    template_name = 'rooms/room_search.html'
    context_object_name = 'rooms'

    def get_queryset(self):

        form = RoomSearchForm(self.request.GET)

        queryset = RoomType.objects.select_related('hotel')

        if not form.is_valid():
            return queryset.none()

        data = form.cleaned_data

        if data.get('city'):
            queryset = queryset.filter(
                hotel__city__icontains=data['city']
            )

        if data.get('capacity'):
            queryset = queryset.filter(
                capacity__gte=data['capacity']
            )

        if data.get('min_price') is not None:
            queryset = queryset.filter(
                price_per_night__gte=data['min_price']
            )

        if data.get('max_price') is not None:
            queryset = queryset.filter(
                price_per_night__lte=data['max_price']
            )

        check_in = data.get('check_in')
        check_out = data.get('check_out')

        rooms_count = data.get('rooms_count') or 1

        if check_in and check_out:

            available_rooms = []

            for room in queryset:

                max_booked = 0

                current_date = check_in

                while current_date < check_out:

                    booked = Booking.objects.filter(
                        room_type=room,
                        status__in=[
                            Booking.Status.PENDING,
                            Booking.Status.CONFIRMED
                        ],
                        check_in__lte=current_date,
                        check_out__gt=current_date
                    ).aggregate(
                        total=Sum('rooms_count')
                    )['total'] or 0

                    max_booked = max(max_booked, booked)

                    current_date += timedelta(days=1)

                room.available_quantity = room.quantity - max_booked

                if room.available_quantity >= rooms_count:
                    available_rooms.append(room)

            return available_rooms

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['form'] = RoomSearchForm(self.request.GET)

        return context

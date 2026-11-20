
from django import forms
from django.db.models import Q

from .models import Booking


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = [
            'check_in',
            'check_out',
            'guests',
            'rooms_count',
        ]

        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, room_type=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_type = room_type

    def clean(self):
        cleaned_data = super().clean()

        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        guests = cleaned_data.get('guests')
        rooms_count = cleaned_data.get('rooms_count')

        if not all([check_in, check_out, guests, rooms_count]):
            return cleaned_data

        if check_out <= check_in:
            self.add_error(
                'check_out',
                'تاریخ خروج باید بعد از تاریخ ورود باشد.'
            )

        if not self.room_type:
            return cleaned_data

        # بررسی ظرفیت مهمان‌ها
        max_capacity = self.room_type.capacity * rooms_count

        if guests > max_capacity:
            self.add_error(
                'guests',
                f'حداکثر ظرفیت این تعداد اتاق {max_capacity} نفر است.'
            )

        # بررسی تعداد اتاق‌های قابل رزرو
        overlapping_bookings = Booking.objects.filter(
            room_type=self.room_type,
            check_in__lt=check_out,
            check_out__gt=check_in,
            status__in=[
                Booking.Status.PENDING,
                Booking.Status.CONFIRMED,
            ]
        )

        reserved_rooms = sum(
            booking.rooms_count
            for booking in overlapping_bookings
        )

        available_rooms = self.room_type.quantity - reserved_rooms

        if rooms_count > available_rooms:
            self.add_error(
                'rooms_count',
                f'فقط {max(available_rooms, 0)} اتاق موجود است.'
            )

        return cleaned_data


class BookingStatusForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ['status']

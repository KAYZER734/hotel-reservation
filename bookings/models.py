from django.conf import settings
from django.db import models
from django.db.models import Q, F
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Booking(models.Model):

    class Status(models.TextChoices):
        PENDING = 'pending', 'در انتظار تأیید'
        CONFIRMED = 'confirmed', 'تأیید شده'
        CANCELLED = 'cancelled', 'لغو شده'
        COMPLETED = 'completed', 'تکمیل شده'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='bookings',
        verbose_name='مشتری'
    )

    room_type = models.ForeignKey(
        'rooms.RoomType',
        on_delete=models.PROTECT,
        related_name='bookings',
        verbose_name='نوع اتاق'
    )

    check_in = models.DateField(
        verbose_name='تاریخ ورود'
    )

    check_out = models.DateField(
        verbose_name='تاریخ خروج'
    )

    guests = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='تعداد مهمان‌ها'
    )

    rooms_count = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='تعداد اتاق'
    )

    total_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name='مبلغ کل'
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='وضعیت رزرو'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ثبت رزرو'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='آخرین تغییر'
    )

def clean(self):
    super().clean()

    errors = {}

    # بررسی تاریخ ورود و خروج
    if self.check_in and self.check_out:
        if self.check_out <= self.check_in:
            errors['check_out'] = 'تاریخ خروج باید بعد از تاریخ ورود باشد.'

    # بررسی ظرفیت اتاق‌ها
    if self.room_type_id and self.guests and self.rooms_count:
        max_capacity = self.room_type.capacity * self.rooms_count

        if self.guests > max_capacity:
            errors['guests'] = (
                f'ظرفیت مجموع اتاق‌های انتخاب‌شده '
                f'{max_capacity} نفر است.'
            )

    if errors:
        raise ValidationError(errors)

    def __str__(self):
        return f'Reservation #{self.pk} - {self.user.username}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'رزرو'
        verbose_name_plural = 'رزروها'
        constraints = [
    models.CheckConstraint(
        condition=Q(check_out__gt=F('check_in')),
        name='booking_checkout_after_checkin'
    )
]
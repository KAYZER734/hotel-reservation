from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.conf import settings
from hotels.models import Hotel



class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name='ایمیل'
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='شماره تلفن'
    )

    def __str__(self):
        return self.username

class HotelAdminRequest(models.Model):

    class Status(models.TextChoices):
        PENDING = 'pending', 'در انتظار بررسی'
        APPROVED = 'approved', 'تأیید شده'
        REJECTED = 'rejected', 'رد شده'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hotel_admin_requests',
        verbose_name='درخواست‌دهنده'
    )

    hotel = models.ForeignKey(
    'hotels.Hotel',
    on_delete=models.CASCADE,
    related_name='admin_requests',
    verbose_name='هتل'
)

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='وضعیت درخواست'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ثبت درخواست'
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='تاریخ بررسی'
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_hotel_admin_requests',
        verbose_name='بررسی‌کننده'
    )

    admin_note = models.TextField(
        blank=True,
        verbose_name='توضیحات مدیر کل'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'hotel'],
                condition=Q(status='pending'),
                name='unique_pending_hotel_admin_request'
            )
        ]

        verbose_name = 'درخواست مدیریت هتل'
        verbose_name_plural = 'درخواست‌های مدیریت هتل'

    def __str__(self):
        return f'{self.user.username} - {self.hotel.name}'
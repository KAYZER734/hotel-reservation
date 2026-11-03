from django.conf import settings
from django.db import models


class Hotel(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='نام هتل'
    )

    city = models.CharField(
        max_length=100,
        verbose_name='شهر'
    )

    address = models.TextField(
        verbose_name='آدرس'
    )

    description = models.TextField(
        blank=True,
        verbose_name='توضیحات'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ثبت'
    )

    def __str__(self):
        return self.name


class HotelAdmin(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hotel_adminships',
        verbose_name='کاربر'
    )

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='administrators',
        verbose_name='هتل'
    )

    assigned_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ اعطای دسترسی'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='دسترسی فعال'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'hotel'],
                name='unique_hotel_admin'
            )
        ]
        verbose_name = 'مدیر هتل'
        verbose_name_plural = 'مدیران هتل'

    def __str__(self):
        return f'{self.user.username} - {self.hotel.name}'

class HotelRegistrationRequest(models.Model):

    class Status(models.TextChoices):
        PENDING = 'pending', 'در انتظار بررسی'
        APPROVED = 'approved', 'تأیید شده'
        REJECTED = 'rejected', 'رد شده'

    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hotel_registration_requests',
        verbose_name='درخواست‌دهنده'
    )

    name = models.CharField(
        max_length=200,
        verbose_name='نام هتل'
    )

    city = models.CharField(
        max_length=100,
        verbose_name='شهر'
    )

    address = models.TextField(
        verbose_name='آدرس'
    )

    description = models.TextField(
        blank=True,
        verbose_name='توضیحات'
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
        related_name='reviewed_hotel_registration_requests',
        verbose_name='بررسی‌کننده'
    )

    admin_note = models.TextField(
        blank=True,
        verbose_name='توضیحات مدیر کل'
    )

    class Meta:
        verbose_name = 'درخواست ثبت هتل'
        verbose_name_plural = 'درخواست‌های ثبت هتل'

    def __str__(self):
        return f'{self.name} - {self.city}'
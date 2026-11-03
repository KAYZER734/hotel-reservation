from django.db import models


class RoomType(models.Model):

    hotel = models.ForeignKey(
        'hotels.Hotel',
        on_delete=models.CASCADE,
        related_name='room_types',
        verbose_name='هتل'
    )

    title = models.CharField(
        max_length=150,
        verbose_name='عنوان اتاق'
    )

    capacity = models.PositiveSmallIntegerField(
        verbose_name='ظرفیت اتاق'
    )

    price_per_night = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='قیمت هر شب'
    )

    features = models.TextField(
        blank=True,
        verbose_name='امکانات اتاق'
    )

    quantity = models.PositiveIntegerField(
        verbose_name='تعداد کل اتاق‌ها'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ثبت'
    )

    def __str__(self):
        return f'{self.title} - {self.hotel.name}'

    class Meta:
        verbose_name = 'نوع اتاق'
        verbose_name_plural = 'انواع اتاق'
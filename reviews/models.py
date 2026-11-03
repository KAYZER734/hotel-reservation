from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='کاربر'
    )

    hotel = models.ForeignKey(
        'hotels.Hotel',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='هتل'
    )

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        verbose_name='امتیاز'
    )

    comment = models.TextField(
        blank=True,
        verbose_name='متن نظر'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ثبت'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='آخرین ویرایش'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'hotel'],
                name='unique_review_per_user_hotel'
            )
        ]

        ordering = ['-created_at']
        verbose_name = 'نظر مشتری'
        verbose_name_plural = 'نظرات مشتریان'

    def __str__(self):
        return f'{self.user.username} - {self.hotel.name} ({self.rating})'
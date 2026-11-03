from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Q
from decimal import Decimal


class Discount(models.Model):

    class DiscountType(models.TextChoices):
        PERCENTAGE = 'percentage', 'درصدی'
        FIXED = 'fixed', 'مبلغ ثابت'

    hotel = models.ForeignKey(
        'hotels.Hotel',
        on_delete=models.CASCADE,
        related_name='discounts',
        verbose_name='هتل'
    )

    code = models.CharField(
        max_length=50,
        verbose_name='کد تخفیف'
    )

    discount_type = models.CharField(
        max_length=10,
        choices=DiscountType.choices,
        verbose_name='نوع تخفیف'
    )

    value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='مقدار تخفیف'
    )

    valid_from = models.DateTimeField(
        verbose_name='شروع اعتبار'
    )

    valid_until = models.DateTimeField(
        verbose_name='پایان اعتبار'
    )

    usage_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='محدودیت تعداد استفاده'
    )

    used_count = models.PositiveIntegerField(
        default=0,
        verbose_name='تعداد استفاده‌شده'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )

    def clean(self):
        super().clean()

        errors = {}

        if self.valid_from and self.valid_until:
            if self.valid_until <= self.valid_from:
                errors['valid_until'] = (
                    'پایان اعتبار باید بعد از شروع اعتبار باشد.'
                )

        if self.discount_type == self.DiscountType.PERCENTAGE:
            if self.value is not None and self.value > 100:
                errors['value'] = 'درصد تخفیف نمی‌تواند بیشتر از ۱۰۰ باشد.'

        if self.usage_limit is not None:
            if self.used_count > self.usage_limit:
                errors['usage_limit'] = (
                    'محدودیت استفاده نمی‌تواند کمتر از تعداد استفاده‌شده باشد.'
                )

        if errors:
            raise ValidationError(errors)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['hotel', 'code'],
                name='unique_discount_code_per_hotel'
            ),
            models.CheckConstraint(
                condition=Q(valid_until__gt=models.F('valid_from')),
                name='discount_valid_until_after_valid_from'
            ),
        ]

        ordering = ['-created_at']
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کدهای تخفیف'

    def __str__(self):
        return f'{self.code} - {self.hotel.name}'
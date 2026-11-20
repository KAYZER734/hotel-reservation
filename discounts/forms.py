
from django import forms
from .models import Discount


class DiscountForm(forms.ModelForm):

    class Meta:
        model = Discount

        fields = [
            'code',
            'discount_type',
            'value',
            'valid_from',
            'valid_until',
            'usage_limit',
            'is_active',
        ]

        labels = {
            'code': 'کد تخفیف',
            'discount_type': 'نوع تخفیف',
            'value': 'مقدار تخفیف',
            'valid_from': 'شروع اعتبار',
            'valid_until': 'پایان اعتبار',
            'usage_limit': 'محدودیت تعداد استفاده',
            'is_active': 'فعال بودن کد تخفیف',
        }

        widgets = {
            'valid_from': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),

            'valid_until': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

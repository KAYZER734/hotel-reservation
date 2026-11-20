
from django import forms
from .models import RoomType


class RoomTypeForm(forms.ModelForm):

    class Meta:
        model = RoomType

        fields = [
            'title',
            'capacity',
            'price_per_night',
            'features',
            'quantity',
        ]


class RoomSearchForm(forms.Form):

    city = forms.CharField(
        required=False,
        label='شهر'
    )

    capacity = forms.IntegerField(
        required=False,
        min_value=1,
        label='ظرفیت موردنیاز'
    )

    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        label='حداقل قیمت'
    )

    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        label='حداکثر قیمت'
    )

    check_in = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='تاریخ ورود'
    )

    check_out = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='تاریخ خروج'
    )

    rooms_count = forms.IntegerField(
        required=False,
        min_value=1,
        initial=1,
        label='تعداد اتاق موردنیاز'
    )

    def clean(self):

        cleaned_data = super().clean()

        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')

        if check_in and check_out and check_out <= check_in:
            self.add_error(
                'check_out',
                'تاریخ خروج باید بعد از تاریخ ورود باشد.'
            )

        if bool(check_in) != bool(check_out):
            raise forms.ValidationError(
                'تاریخ ورود و خروج را با هم وارد کنید.'
            )

        if min_price is not None and max_price is not None:
            if max_price < min_price:
                self.add_error(
                    'max_price',
                    'حداکثر قیمت نباید کمتر از حداقل قیمت باشد.'
                )

        return cleaned_data

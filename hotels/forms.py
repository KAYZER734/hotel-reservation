
from django import forms

from .models import HotelRegistrationRequest


class HotelRegistrationRequestForm(forms.ModelForm):

    class Meta:
        model = HotelRegistrationRequest

        fields = [
            'name',
            'city',
            'address',
            'description',
        ]

        labels = {
            'name': 'نام هتل',
            'city': 'شهر',
            'address': 'آدرس کامل',
            'description': 'توضیحات هتل',
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'نام هتل را وارد کنید'
            }),

            'city': forms.TextInput(attrs={
                'placeholder': 'شهر محل هتل را وارد کنید'
            }),

            'address': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'آدرس کامل هتل را وارد کنید'
            }),

            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'توضیحات هتل را وارد کنید'
            }),
        }

from django import forms
from .models import HotelAdmin
from django.contrib.auth import get_user_model


User = get_user_model()


class HotelAdminForm(forms.ModelForm):

    class Meta:
        model = HotelAdmin
        fields = ['user']
        labels = {
            'user': 'انتخاب کاربر',
        }

    def __init__(self, *args, **kwargs):
        self.hotel = kwargs.pop('hotel')
        super().__init__(*args, **kwargs)

        # کاربرانی که هنوز مدیر این هتل نیستند
        self.fields['user'].queryset = User.objects.exclude(
            hotel_adminships__hotel=self.hotel
        )

from django import forms
from .models import HotelRegistrationRequest


class HotelRegistrationRequestForm(forms.ModelForm):

    class Meta:
        model = HotelRegistrationRequest
        fields = [
            'name',
            'city',
            'address',
            'description',
        ]

        labels = {
            'name': 'نام هتل',
            'city': 'شهر',
            'address': 'آدرس',
            'description': 'توضیحات',
        }

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

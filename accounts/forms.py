
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, HotelAdminRequest
from hotels.models import Hotel, HotelAdmin


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
        ]


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
        ]


class HotelAdminRequestForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    class Meta:
        model = HotelAdminRequest
        fields = ['hotel']

    def clean_hotel(self):
        hotel = self.cleaned_data['hotel']

        # بررسی درخواست در انتظار
        if HotelAdminRequest.objects.filter(
            user=self.user,
            hotel=hotel,
            status=HotelAdminRequest.Status.PENDING
        ).exists():
            raise forms.ValidationError(
                'برای این هتل قبلاً درخواست ثبت کرده‌اید.'
            )

        # بررسی مدیر بودن کاربر
        if HotelAdmin.objects.filter(
            user=self.user,
            hotel=hotel,
            is_active=True
        ).exists():
            raise forms.ValidationError(
                'شما در حال حاضر مدیر این هتل هستید.'
            )

        return hotel


class HotelAdminReviewForm(forms.ModelForm):

    status = forms.ChoiceField(
        choices=[
            (HotelAdminRequest.Status.APPROVED, 'تأیید درخواست'),
            (HotelAdminRequest.Status.REJECTED, 'رد درخواست'),
        ],
        label='وضعیت درخواست'
    )

    class Meta:
        model = HotelAdminRequest
        fields = ['status', 'admin_note']

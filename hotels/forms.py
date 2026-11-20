
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


class HotelRegistrationReviewForm(forms.ModelForm):

    class Meta:
        model = HotelRegistrationRequest

        fields = [
            'status',
            'admin_note',
        ]

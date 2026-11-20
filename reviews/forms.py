
from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['rating', 'comment']

        labels = {
            'rating': 'امتیاز هتل',
            'comment': 'نظر شما',
        }

        widgets = {
            'rating': forms.Select(
                choices=[
                    (1, '۱ - خیلی ضعیف'),
                    (2, '۲ - ضعیف'),
                    (3, '۳ - متوسط'),
                    (4, '۴ - خوب'),
                    (5, '۵ - عالی'),
                ]
            ),
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'نظر خود را درباره هتل بنویسید...'
            }),
        }

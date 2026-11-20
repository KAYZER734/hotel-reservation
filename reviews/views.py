
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages

from .models import Review
from .forms import ReviewForm
from hotels.models import Hotel


# نمایش نظرات یک هتل
class ReviewListView(ListView):

    model = Review
    template_name = 'reviews/review_list.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        self.hotel = get_object_or_404(
            Hotel,
            pk=self.kwargs['hotel_pk']
        )

        return Review.objects.filter(
            hotel=self.hotel
        ).select_related('user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel'] = self.hotel
        return context


# ثبت نظر برای هتل
class ReviewCreateView(LoginRequiredMixin, CreateView):

    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.hotel = get_object_or_404(
            Hotel,
            pk=self.kwargs['hotel_pk']
        )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        existing_review = Review.objects.filter(
            user=request.user,
            hotel=self.hotel
        ).first()

        if existing_review:
            return redirect(
                'reviews:review_update',
                pk=existing_review.pk
            )

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.hotel = self.hotel

        messages.success(self.request, 'نظر شما با موفقیت ثبت شد.')

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'reviews:review_list',
            kwargs={'hotel_pk': self.hotel.pk}
        )


# ویرایش نظر
class ReviewUpdateView(LoginRequiredMixin, UpdateView):

    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def get_queryset(self):
        return Review.objects.filter(
            user=self.request.user
        )

    def get_success_url(self):
        return reverse(
            'reviews:review_list',
            kwargs={'hotel_pk': self.object.hotel.pk}
        )


# حذف نظر
class ReviewDeleteView(LoginRequiredMixin, DeleteView):

    model = Review
    template_name = 'reviews/review_confirm_delete.html'

    def get_queryset(self):
        return Review.objects.filter(
            user=self.request.user
        )

    def get_success_url(self):
        return reverse(
            'reviews:review_list',
            kwargs={'hotel_pk': self.object.hotel.pk}
        )

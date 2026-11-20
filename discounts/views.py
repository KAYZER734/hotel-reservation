
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages

from .models import Discount
from .forms import DiscountForm
from hotels.models import HotelAdmin


# بررسی دسترسی مدیر هتل
class HotelManagerRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):

        self.hotel_admin = get_object_or_404(
            HotelAdmin,
            user=request.user,
            hotel_id=kwargs['hotel_pk'],
            is_active=True
        )

        return super().dispatch(request, *args, **kwargs)


# نمایش کدهای تخفیف هتل
class DiscountListView(HotelManagerRequiredMixin, ListView):

    model = Discount
    template_name = 'discounts/discount_list.html'
    context_object_name = 'discounts'

    def get_queryset(self):

        return Discount.objects.filter(
            hotel=self.hotel_admin.hotel
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['hotel'] = self.hotel_admin.hotel

        return context


# ایجاد کد تخفیف
class DiscountCreateView(HotelManagerRequiredMixin, CreateView):

    model = Discount
    form_class = DiscountForm
    template_name = 'discounts/discount_form.html'

    def form_valid(self, form):

        form.instance.hotel = self.hotel_admin.hotel

        messages.success(
            self.request,
            'کد تخفیف با موفقیت ایجاد شد.'
        )

        return super().form_valid(form)

    def get_success_url(self):

        return reverse(
            'discounts:discount_list',
            kwargs={'hotel_pk': self.hotel_admin.hotel.pk}
        )


# ویرایش کد تخفیف
class DiscountUpdateView(HotelManagerRequiredMixin, UpdateView):

    model = Discount
    form_class = DiscountForm
    template_name = 'discounts/discount_form.html'

    def get_queryset(self):

        return Discount.objects.filter(
            hotel=self.hotel_admin.hotel
        )

    def get_success_url(self):

        return reverse(
            'discounts:discount_list',
            kwargs={'hotel_pk': self.hotel_admin.hotel.pk}
        )


# حذف کد تخفیف
class DiscountDeleteView(HotelManagerRequiredMixin, DeleteView):

    model = Discount
    template_name = 'discounts/discount_confirm_delete.html'

    def get_queryset(self):

        return Discount.objects.filter(
            hotel=self.hotel_admin.hotel
        )

    def get_success_url(self):

        return reverse(
            'discounts:discount_list',
            kwargs={'hotel_pk': self.hotel_admin.hotel.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['hotel_pk'] = self.hotel_admin.hotel.pk

        return context
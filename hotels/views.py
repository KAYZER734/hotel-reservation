
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone

from .models import Hotel, HotelAdmin, HotelRegistrationRequest

from .forms import (
    HotelRegistrationRequestForm,
    HotelRegistrationReviewForm
)


# نمایش فهرست هتل ها
class HotelListView(ListView):

    model = Hotel
    template_name = 'hotels/hotel_list.html'
    context_object_name = 'hotels'


# نمایش جزئیات یک هتل
class HotelDetailView(DetailView):

    model = Hotel
    template_name = 'hotels/hotel_detail.html'
    context_object_name = 'hotel'


# ثبت درخواست ایجاد هتل
class HotelRequestCreateView(LoginRequiredMixin, CreateView):

    model = HotelRegistrationRequest
    form_class = HotelRegistrationRequestForm

    template_name = 'hotels/hotel_request.html'

    success_url = reverse_lazy('hotels:my_hotel_requests')

    def form_valid(self, form):

        form.instance.submitted_by = self.request.user

        return super().form_valid(form)


# مشاهده درخواست های ثبت هتل توسط کاربر
class MyHotelRequestsView(LoginRequiredMixin, ListView):

    model = HotelRegistrationRequest

    template_name = 'hotels/my_hotel_requests.html'

    context_object_name = 'requests'

    def get_queryset(self):

        return HotelRegistrationRequest.objects.filter(
            submitted_by=self.request.user
        ).order_by('-created_at')


# بررسی دسترسی مدیر کل
class SuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):

        return self.request.user.is_superuser


# مشاهده تمام درخواست های ثبت هتل
class AdminHotelRequestsView(SuperuserRequiredMixin, ListView):

    model = HotelRegistrationRequest

    template_name = 'hotels/admin_hotel_requests.html'

    context_object_name = 'requests'

    ordering = ['-created_at']


# بررسی و تأیید یا رد درخواست ثبت هتل
class HotelRequestReviewView(SuperuserRequiredMixin, UpdateView):

    model = HotelRegistrationRequest

    form_class = HotelRegistrationReviewForm

    template_name = 'hotels/review_hotel_request.html'

    success_url = reverse_lazy('hotels:admin_hotel_requests')

    def get_queryset(self):

        return HotelRegistrationRequest.objects.filter(
            status=HotelRegistrationRequest.Status.PENDING
        )

    def form_valid(self, form):

        request_obj = form.save(commit=False)

        request_obj.reviewed_by = self.request.user

        request_obj.reviewed_at = timezone.now()

        request_obj.save()

        # در صورت تأیید درخواست، هتل ساخته می شود
        if request_obj.status == HotelRegistrationRequest.Status.APPROVED:

            hotel = Hotel.objects.create(
                name=request_obj.name,
                city=request_obj.city,
                address=request_obj.address,
                description=request_obj.description
            )

            # ثبت درخواست دهنده به عنوان مدیر هتل
            HotelAdmin.objects.get_or_create(
                user=request_obj.submitted_by,
                hotel=hotel,
                defaults={
                    'is_active': True
                }
            )

        return redirect(self.success_url)


# مشاهده هتل های تحت مدیریت کاربر
class MyHotelsView(LoginRequiredMixin, ListView):

    model = Hotel

    template_name = 'hotels/my_hotels.html'

    context_object_name = 'hotels'

    def get_queryset(self):

        return Hotel.objects.filter(
            administrators__user=self.request.user,
            administrators__is_active=True
        ).distinct()


from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    TemplateView,
    UpdateView,
    ListView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.utils import timezone

from .models import User, HotelAdminRequest
from .forms import (
    UserRegisterForm,
    ProfileForm,
    HotelAdminRequestForm,
    HotelAdminReviewForm
)

from hotels.models import HotelAdmin


# ثبت نام کاربر
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')


# ورود کاربر
class UserLoginView(LoginView):
    template_name = 'registration/login.html'


# خروج کاربر
class UserLogoutView(LogoutView):
    pass


# مشاهده پروفایل
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'


# ویرایش پروفایل
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user


# ثبت درخواست مدیریت هتل
class HotelAdminRequestCreateView(LoginRequiredMixin, CreateView):
    model = HotelAdminRequest
    form_class = HotelAdminRequestForm
    template_name = 'accounts/hotel_admin_request.html'
    success_url = reverse_lazy('accounts:my_requests')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# مشاهده درخواست های خود کاربر
class MyHotelAdminRequestsView(LoginRequiredMixin, ListView):
    model = HotelAdminRequest
    template_name = 'accounts/my_requests.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return HotelAdminRequest.objects.filter(
            user=self.request.user
        ).order_by('-created_at')


# بررسی دسترسی مدیر کل
class SuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser


# مشاهده تمام درخواست های مدیریت هتل توسط مدیر کل
class AdminHotelAdminRequestsView(
    SuperuserRequiredMixin,
    ListView
):
    model = HotelAdminRequest
    template_name = 'accounts/admin_requests.html'
    context_object_name = 'requests'
    ordering = ['-created_at']


# بررسی و تأیید یا رد درخواست
class HotelAdminRequestReviewView(
    SuperuserRequiredMixin,
    UpdateView
):
    model = HotelAdminRequest
    form_class = HotelAdminReviewForm
    template_name = 'accounts/review_request.html'
    success_url = reverse_lazy('accounts:admin_requests')

    def get_queryset(self):
        return HotelAdminRequest.objects.filter(
            status=HotelAdminRequest.Status.PENDING
        )

    def form_valid(self, form):

        request_obj = form.save(commit=False)

        request_obj.reviewed_by = self.request.user
        request_obj.reviewed_at = timezone.now()

        request_obj.save()

        # اگر درخواست تأیید شد، کاربر مدیر هتل می شود
        if request_obj.status == HotelAdminRequest.Status.APPROVED:

            admin, created = HotelAdmin.objects.get_or_create(
                user=request_obj.user,
                hotel=request_obj.hotel,
                defaults={'is_active': True}
            )

            # فعال کردن دسترسی قبلی در صورت غیرفعال بودن
            if not created and not admin.is_active:
                admin.is_active = True
                admin.save()

        return redirect(self.success_url)

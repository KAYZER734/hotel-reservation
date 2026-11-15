
from .models import Hotel, HotelAdmin, HotelRegistrationRequest
from django.views.generic import ListView, DetailView
from .models import Hotel
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import HotelRegistrationRequestForm
from .models import HotelRegistrationRequest



class HotelListView(ListView):
    model = Hotel
    template_name = 'hotels/hotel_list.html'
    context_object_name = 'hotels'

    def get_queryset(self):
        # دریافت عبارت جست‌وجو از آدرس صفحه
        search_query = self.request.GET.get('q', '').strip()

        # دریافت شهر انتخاب‌شده
        selected_city = self.request.GET.get('city', '').strip()

        # دریافت تمام هتل‌ها
        queryset = Hotel.objects.all()

        # جست‌وجو در نام، شهر و توضیحات هتل
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(city__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        # فیلتر بر اساس شهر
        if selected_city:
            queryset = queryset.filter(city=selected_city)

        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # دریافت شهرهای موجود در پایگاه داده
        context['cities'] = (
            Hotel.objects
            .order_by('city')
            .values_list('city', flat=True)
            .distinct()
        )

        # نگهداری مقادیر انتخاب‌شده در فرم
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_city'] = self.request.GET.get('city', '')

        return context


class HotelDetailView(DetailView):
    model = Hotel
    template_name = 'hotels/hotel_detail.html'
    context_object_name = 'hotel'


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import HotelRegistrationRequest


class MyHotelRequestsView(LoginRequiredMixin, ListView):
    model = HotelRegistrationRequest
    template_name = 'hotels/my_requests.html'
    context_object_name = 'requests'
    ordering = ['-created_at']

    def get_queryset(self):
        return HotelRegistrationRequest.objects.filter(
            submitted_by=self.request.user
        ).order_by('-created_at')


from django.views.generic import DetailView
from django.db.models import Q


class HotelRequestDetailView(LoginRequiredMixin, DetailView):
    model = HotelRegistrationRequest
    template_name = 'hotels/request_detail.html'
    context_object_name = 'hotel_request'

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return HotelRegistrationRequest.objects.all()

        return HotelRegistrationRequest.objects.filter(
            submitted_by=user
        )


from django.contrib.auth.mixins import UserPassesTestMixin


class AdminHotelRequestsView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    ListView
):
    model = HotelRegistrationRequest
    template_name = 'hotels/admin_requests.html'
    context_object_name = 'requests'
    ordering = ['-created_at']

    def test_func(self):
        return self.request.user.is_superuser

from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from django.utils import timezone
from django.http import HttpResponseBadRequest

class ReviewHotelRequestView(LoginRequiredMixin,UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, pk):

        with transaction.atomic():

            hotel_request = get_object_or_404(
                HotelRegistrationRequest.objects.select_for_update(),
                pk=pk
            )

            if hotel_request.status != HotelRegistrationRequest.Status.PENDING:
                return redirect('hotels:admin_requests')

            action = request.POST.get('action')
            admin_note = request.POST.get('admin_note', '')

            if action == 'approve':

                hotel = Hotel.objects.create(
                    name=hotel_request.name,
                    city=hotel_request.city,
                    address=hotel_request.address,
                    description=hotel_request.description
                )

                HotelAdmin.objects.create(
                    user=hotel_request.submitted_by,
                    hotel=hotel
                )

                hotel_request.status = HotelRegistrationRequest.Status.APPROVED

            elif action == 'reject':

                hotel_request.status = HotelRegistrationRequest.Status.REJECTED

            else:
                return HttpResponseBadRequest('عملیات نامعتبر است.')

            hotel_request.reviewed_by = request.user
            hotel_request.reviewed_at = timezone.now()
            hotel_request.admin_note = admin_note

            hotel_request.save()

        return redirect('hotels:admin_requests')


from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import HotelRegistrationRequestForm
from .models import HotelRegistrationRequest


class HotelRequestCreateView(LoginRequiredMixin, CreateView):

    model = HotelRegistrationRequest
    form_class = HotelRegistrationRequestForm
    template_name = 'hotels/hotel_request_form.html'
    success_url = reverse_lazy('hotels:my_requests')

    def form_valid(self, form):
        form.instance.submitted_by = self.request.user
        return super().form_valid(form)


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Hotel

class MyManagedHotelsView(LoginRequiredMixin, ListView):

    model = Hotel
    template_name = 'hotels/my_managed_hotels.html'
    context_object_name = 'hotels'

    def get_queryset(self):
        return Hotel.objects.filter(
            administrators__user=self.request.user,
            administrators__is_active=True
        ).distinct().order_by('name')

from django.views.generic import UpdateView
from django.urls import reverse


# ویرایش اطلاعات هتل توسط مدیر همان هتل
class HotelUpdateView(LoginRequiredMixin, UpdateView):

    model = Hotel
    template_name = 'hotels/hotel_update.html'
    context_object_name = 'hotel'

    # فقط این فیلدها اجازه ویرایش دارند
    fields = [
        'name',
        'city',
        'address',
        'description',
    ]

    def get_queryset(self):
        # فقط هتل‌هایی که کاربر مدیر فعال آن‌هاست
        return Hotel.objects.filter(
            administrators__user=self.request.user,
            administrators__is_active=True
        ).distinct()

    def get_success_url(self):
        # پس از ویرایش، رفتن به صفحه جزئیات همان هتل
        return reverse(
            'hotels:hotel_detail',
            kwargs={'pk': self.object.pk}
        )

from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.views.generic import DeleteView

# حذف هتل توسط مدیر همان هتل
class HotelDeleteView(LoginRequiredMixin, DeleteView):

    model = Hotel
    template_name = 'hotels/hotel_confirm_delete.html'
    context_object_name = 'hotel'
    success_url = reverse_lazy('hotels:hotel_list')

    # فقط مدیر فعال همان هتل اجازه حذف دارد
    def get_queryset(self):
        return Hotel.objects.filter(
            administrators__user=self.request.user,
            administrators__is_active=True
        ).distinct()

    # بررسی وجود رزرو قبل از حذف
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        has_bookings = self.object.room_types.filter(
            bookings__isnull=False
        ).exists()

        if has_bookings:
            messages.error(
                request,
                'این هتل دارای رزرو است و امکان حذف آن وجود ندارد.'
            )
            return redirect(
                'hotels:hotel_detail',
                pk=self.object.pk
            )

        try:
            return super().post(request, *args, **kwargs)

        except ProtectedError:
            # محافظت در برابر ثبت رزرو هم‌زمان با درخواست حذف
            messages.error(
                request,
                'به دلیل وجود رزرو مرتبط، امکان حذف این هتل وجود ندارد.'
            )
            return redirect(
                'hotels:hotel_detail',
                pk=self.object.pk
            )

from django.urls import reverse
from django.views.generic import CreateView, DeleteView
from .forms import HotelAdminForm

# مشاهده مدیران یک هتل
class HotelAdminListView(LoginRequiredMixin, ListView):

    model = HotelAdmin
    template_name = 'hotels/hotel_admin_list.html'
    context_object_name = 'hotel_admins'

    def dispatch(self, request, *args, **kwargs):
        self.hotel = get_object_or_404(
            Hotel,
            pk=kwargs['pk'],
            administrators__user=request.user,
            administrators__is_active=True
        )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return HotelAdmin.objects.filter(
            hotel=self.hotel
        ).select_related('user').order_by('assigned_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel'] = self.hotel
        return context


# اضافه کردن مدیر جدید به هتل
class HotelAdminCreateView(LoginRequiredMixin, CreateView):

    model = HotelAdmin
    form_class = HotelAdminForm
    template_name = 'hotels/hotel_admin_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.hotel = get_object_or_404(
            Hotel,
            pk=kwargs['pk'],
            administrators__user=request.user,
            administrators__is_active=True
        )
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['hotel'] = self.hotel
        return kwargs

    def form_valid(self, form):
        form.instance.hotel = self.hotel
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'hotels:hotel_admins',
            kwargs={'pk': self.hotel.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel'] = self.hotel
        return context


# حذف دسترسی مدیریتی یک کاربر از هتل
class HotelAdminDeleteView(LoginRequiredMixin, DeleteView):

    model = HotelAdmin
    template_name = 'hotels/hotel_admin_confirm_delete.html'
    context_object_name = 'hotel_admin'

    def dispatch(self, request, *args, **kwargs):
        self.hotel = get_object_or_404(
            Hotel,
            pk=kwargs['pk'],
            administrators__user=request.user,
            administrators__is_active=True
        )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return HotelAdmin.objects.filter(
            hotel=self.hotel
        ).select_related('user')

    def get_object(self, queryset=None):
        return get_object_or_404(
            self.get_queryset(),
            pk=self.kwargs['admin_pk']
        )

    def get_success_url(self):
        return reverse(
            'hotels:hotel_admins',
            kwargs={'pk': self.hotel.pk}
        )
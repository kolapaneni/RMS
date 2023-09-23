from datetime import datetime

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from .models import RoomRate, OverriddenRoomRate, Discount, DiscountRoomRate, DiscountTypeChoices
from .forms import RoomRateForm, OverriddenRoomRateForm, DiscountForm, DiscountRoomRateForm, FilterForm


def homepage(request):
    return render(request=request, template_name='room/base.html')


class RoomRateCreateView(CreateView):
    model = RoomRate
    form_class = RoomRateForm
    template_name = 'room/room_rate.html'
    success_url = reverse_lazy('room_rate_list')


class RoomRateUpdateView(UpdateView):
    model = RoomRate
    form_class = RoomRateForm
    template_name = 'room/room_rate.html'
    success_url = reverse_lazy('room_rate_list')


class RoomRateDeleteView(DeleteView):
    model = RoomRate
    template_name = 'room/delete_room.html'
    success_url = reverse_lazy('room_rate_list')


class RoomRateListView(ListView):
    model = RoomRate
    template_name = 'room/room_list.html'


# Overridden APIs
class OverriddenCreateView(CreateView):
    model = OverriddenRoomRate
    form_class = OverriddenRoomRateForm
    template_name = 'overriddenroomrate/overridden.html'
    success_url = reverse_lazy('overridden_list')


class OverriddenUpdateView(UpdateView):
    model = OverriddenRoomRate
    form_class = OverriddenRoomRateForm
    template_name = 'overriddenroomrate/overridden.html'
    success_url = reverse_lazy('overridden_list')


class OverriddenDeleteView(DeleteView):
    model = OverriddenRoomRate
    template_name = 'overriddenroomrate/delete_overridden.html'
    success_url = reverse_lazy('overridden_list')


class OverriddenListView(ListView):
    model = OverriddenRoomRate
    template_name = 'overriddenroomrate/overridden_list.html'


# Discount APIs
class DiscountCreateView(CreateView):
    model = Discount
    form_class = DiscountForm
    template_name = 'discount/create_discount.html'
    success_url = reverse_lazy('discount_list')


class DiscountUpdateView(UpdateView):
    model = Discount
    form_class = DiscountForm
    template_name = 'discount/create_discount.html'
    success_url = reverse_lazy('discount_list')


class DiscountDeleteView(DeleteView):
    model = Discount
    template_name = 'discount/delete_discount.html'
    success_url = reverse_lazy('discount_list')


class DiscountListView(ListView):
    model = Discount
    template_name = 'discount/discount_list.html'


# Room Rate and Discount Mapping
class DiscountRoomRateCreateView(CreateView):
    model = DiscountRoomRate
    form_class = DiscountRoomRateForm
    template_name = 'discount_room_rate/create_discount_room_rate.html'
    success_url = reverse_lazy('discount_rate_list')


class DiscountRoomRateUpdateView(UpdateView):
    model = DiscountRoomRate
    form_class = DiscountRoomRateForm
    template_name = 'discount_room_rate/create_discount_room_rate.html'
    success_url = reverse_lazy('discount_rate_list')


class DiscountRoomRateDeleteView(DeleteView):
    model = DiscountRoomRate
    template_name = 'discount_room_rate/delete_discount_room.html'
    success_url = reverse_lazy('discount_rate_list')


class DiscountRoomRateListView(ListView):
    model = DiscountRoomRate
    template_name = 'discount_room_rate/discount_room_list.html'


class CalculateFinalRate(View):
    def get(self, request, room_id, start_date, end_date):
        print(start_date, type(start_date))
        start_day = datetime.strptime(start_date, '%Y-%m-%d')
        end_day = datetime.strptime(end_date, '%Y-%m-%d')

        default_rate = RoomRate.objects.get(room_id=room_id).default_rate

        room_rate_dict = {}
        for date in range(start_day.day, end_day.day+1):
            room_rate_dict[date] = default_rate

        overridden_rates = OverriddenRoomRate.objects.filter(
            room_rate__room_id=room_id,
            stay_date__range=[start_date, end_date]
        )

        if overridden_rates.exists():
            print("overridden rates======")
            for overridden_rate in overridden_rates:
                print(overridden_rate.overridden_rate)
                room_rate_dict[overridden_rate.stay_date.day] = overridden_rate.overridden_rate

        highest_fixed_discount = DiscountRoomRate.objects.filter(room_rate__room_id=room_id, discount__discount_type=DiscountTypeChoices.FIXED).order_by('discount__discount_value').last()
        if highest_fixed_discount:
            highest_fixed_discount = highest_fixed_discount.discount.discount_value
        highest_percentage_discount = DiscountRoomRate.objects.filter(room_rate__room_id=room_id, discount__discount_type=DiscountTypeChoices.PERCENTAGE).order_by('discount__discount_value').last()

        if highest_percentage_discount:
            highest_percentage_discount = round(highest_percentage_discount.discount.discount_value / 100, 2)

        for date in room_rate_dict.keys():
            rate = room_rate_dict[date]
            fixed_rate = rate
            percentage_rate = rate

            if highest_fixed_discount:
                fixed_rate = rate - highest_fixed_discount

            if highest_percentage_discount:
                percentage_rate = rate - (rate * highest_percentage_discount)
            lowest_rate = min(fixed_rate, percentage_rate)
            if lowest_rate <= 0:
                lowest_rate = 0

            room_rate_dict[date] = lowest_rate

        return render(request, 'calculated_amount/rate_results.html', {
            'room_id': room_id,
            'start_date': start_date,
            'end_date': end_date,
            'final_rate': room_rate_dict,
        })


class FilterRoomRates(View):
    def get(self, request):
        form = FilterForm()
        return render(request, 'calculated_amount/filter_room_rates.html', {'form': form})

    def post(self, request):
        form = FilterForm(request.POST)
        print("Submitted data:", request.POST)
        # print("Available room IDs:", list(form.fields['room_id'].choices))
        if 'room_id' in request.POST and 'start_date' in request.POST and 'end_date' in request.POST:
            room_id = request.POST['room_id']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            print(room_id, start_date, end_date)
            if start_date > end_date:
                form.add_error('end_date', 'End date cannot be earlier than start date')
                return render(request, 'calculated_amount/filter_room_rates.html', {'form': form})

            return redirect('calculate_final_rate', room_id=room_id, start_date=start_date, end_date=end_date)

        return render(request, 'calculated_amount/filter_room_rates.html', {'form': form})

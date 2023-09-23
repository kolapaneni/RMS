from django import forms
from .models import RoomRate, OverriddenRoomRate, Discount, DiscountRoomRate


class RoomRateForm(forms.ModelForm):

    class Meta:
        model = RoomRate
        fields = ['id', 'room_id', 'room_name', 'default_rate']


class OverriddenRoomRateForm(forms.ModelForm):
    stay_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = OverriddenRoomRate
        fields = ['id', 'room_rate', 'overridden_rate', 'stay_date']


class DiscountForm(forms.ModelForm):

    class Meta:
        model = Discount
        fields = ['id', 'discount_id', 'discount_name', 'discount_type', 'discount_value']


class DiscountRoomRateForm(forms.ModelForm):

    class Meta:
        model = DiscountRoomRate
        fields = ['id', 'room_rate', 'discount']


class FilterForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    room_id = forms.ModelChoiceField(queryset=RoomRate.objects.values_list('room_id', flat=True).distinct())

    class Meta:
        model = RoomRate
        fields = ['room_id', 'start_date', 'end_date']

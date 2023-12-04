from django.forms import ModelForm
from django import forms
from LittlelemonAPI.models import Booking


# Code added for loading form data on the Booking page
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['first_name', 'reservation_date', 'reservation_slot']
        widgets = {
            'reservation_date': forms.DateInput(attrs={'type': 'date'}),
        }
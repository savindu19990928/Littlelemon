# from django.http import HttpResponse
from django.shortcuts import render
from .forms import BookingForm
from LittlelemonAPI.models import MenuItem, Booking
from django.core import serializers
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def reservations(request):
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    json_object = json.loads(booking_json)
    bookings_list = list()
    for booking in json_object:
        bookings_list.append(booking)
    return render(request, 'bookings.html',{"bookings":bookings_list})

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)

# Add your code here to create new views
def menu(request):
    menu_data = MenuItem.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


def display_menu_item(request, pk=None): 
    if pk: 
        menu_item = MenuItem.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 

# @csrf_exempt
def bookings(request):
    date = request.GET.get('date',datetime.today().date())
    # formatted_date = date.strftime('%Y-%m-%d') 
    json_param = request.GET.get('date', date)
    # data = json.load(json_param)
    # exist = Booking.objects.filter(reservation_date=data['date']).filter(
    #     reservation_slot=data['reservation_slot']).exists()
    # if exist==False:
    #     booking = Booking(
    #         first_name=data['first_name'],
    #         reservation_date=data['reservation_date'],
    #         reservation_slot=data['reservation_slot'],
    #     )
    #     booking.save()
    bookings = Booking.objects.all().filter(reservation_date=str(json_param))
    booking_json = serializers.serialize('json', bookings)

    return HttpResponse(booking_json, content_type='application/json')
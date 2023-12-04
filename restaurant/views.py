# from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import BookingForm, LoginForm
from LittlelemonAPI.models import MenuItem, Booking
from django.core import serializers
from datetime import datetime
import json
import requests
from django.http import HttpResponse
from rest_framework.authtoken.models import Token

def isauth(request):
    tok = request.COOKIES.get('token', None)
    if tok is not None:
        if Token.objects.get(key=tok):
            return True
        else:
            return False
    else:
        return False

# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def reservations(request):
    if not isauth(request):
        return HttpResponse("You must login or register")
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    json_object = json.loads(booking_json)
    bookings_list = list()
    for booking in json_object:
        bookings_list.append(booking)
    return render(request, 'bookings.html',{"bookings":bookings_list})

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            response = requests.post("http://127.0.0.1:8000/auth/token/login", data=form.data)
            res = HttpResponse()
            res = redirect('http://127.0.0.1:8000/')
            res.set_cookie('token', response.json()["auth_token"])
            return res
    context = {'form':form}
    return render(request, 'login.html', context)

def logout(request):
    tok = request.COOKIES.get('token', None)
    if tok is not None:
        headers = {'Authorization': f'token {tok}',}
        requests.post("http://127.0.0.1:8000/auth/token/logout", headers=headers)
        res = HttpResponse()
        res = redirect('http://127.0.0.1:8000/')
        res.delete_cookie('token')
        return res



def register(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            requests.post("http://127.0.0.1:8000/api/register", data=form.data)
            res = HttpResponse()
            res = redirect('http://127.0.0.1:8000/registeruser')
            return res
    context = {'form':form}
    return render(request, 'login.html', context)

def book(request):
    if not isauth(request):
        return HttpResponse("You must login or register")
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


def bookings(request):
    if not isauth(request):
        return HttpResponse("You must login or register")
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
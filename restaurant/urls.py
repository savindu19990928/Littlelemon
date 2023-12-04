from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('menu/', views.menu, name="menu"),
    path('menu_item/<int:pk>/', views.display_menu_item, name="menu_item"),
    path('reservations/', views.reservations, name="reservations"),
    path('bookings/', views.bookings, name="bookings"),
    path('loginuser/', views.login, name="loginuser"),
    path('registeruser/', views.register, name="registeruser"),
    path('logoutuser/', views.logout, name="logoutuser"),
    path('api-token-auth/', obtain_auth_token),
]
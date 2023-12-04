from django.contrib import admin

# Register your models here.
from .models import Booking, MenuItem, Category

admin.site.register(Booking)
admin.site.register(MenuItem)
admin.site.register(Category)
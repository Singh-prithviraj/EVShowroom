from django.contrib import admin

# Register your models here.
from django.contrib import admin 
from .models import Bike, TestRideBooking

@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'available')
    list_filter = ('brand', 'available')
    search_fields = ('name', 'brand')

@admin.register(TestRideBooking)
class TestRideBookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'bike', 'preferred_date', 'phone')
    list_filter = ('preferred_date', 'bike')
    search_fields = ('customer_name', 'bike__name')

from django.contrib import admin
from .models import BikeBooking

@admin.register(BikeBooking)
class BikeBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'bike_model', 'booking_date', 'email', 'created_at')
    search_fields = ('name', 'bike_model', 'email')

from django.contrib import admin
from .models import Bike, TestRideBooking, ContactMessage, BikePurchase, Profile, Booking

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


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email')


@admin.register(BikePurchase)
class BikePurchaseAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'bike', 'email', 'phone', 'date')
    search_fields = ('customer_name', 'bike__name')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "bike", "preferred_date", "preferred_time", "status")
    list_filter = ("status", "preferred_date")
    search_fields = ("customer_name", "email", "phone")

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# -------------------------
# BIKE MODEL
# -------------------------
class Bike(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    range_km = models.PositiveIntegerField()
    battery_capacity = models.CharField(max_length=50)
    top_speed = models.PositiveIntegerField()
    image = models.ImageField(upload_to='bikes/')
    description = models.TextField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.brand} - {self.name}"


# -------------------------
# TEST RIDE BOOKING
# -------------------------
class TestRideBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name='test_ride_bookings')
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    preferred_date = models.DateField()
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.bike.name}"


# -------------------------
# CONTACT FORM
# -------------------------
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


# -------------------------
# FULL BIKE PURCHASE
# -------------------------
class BikePurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    color = models.CharField(max_length=50)
    variant = models.CharField(max_length=50, default="Standard")
    address = models.TextField()
    payment_mode = models.CharField(max_length=50, choices=[('COD', 'Cash on Delivery'), ('Online', 'Online Payment')])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.bike.name}"


# -------------------------
# USER PROFILE
# -------------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        Profile.objects.get_or_create(user=instance)


# -------------------------
# BIKE BOOKING SYSTEM (new)
# -------------------------
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    BOOKING_TYPES = (
        ('pre_book', 'Pre-Booking'),
    )

    STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )

    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100, default="Unknown")
    state = models.CharField(max_length=100, default="Unknown")
    pincode = models.CharField(max_length=6, null=True, blank=True)
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPES)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.bike.name}"

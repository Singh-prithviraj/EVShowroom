from django.db import models
from django.contrib.auth.models import User

# Create your models here.


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

# bike booking model
class TestRideBooking(models.Model):
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name='bookings')
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    preferred_date = models.DateField()
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.bike.name}"


#contact 

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

# booking 

class BikeBooking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    bike_model = models.CharField(max_length=100)
    booking_date = models.DateField()
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.bike_model}"

# buy section


class BikePurchase(models.Model):
    bike = models.ForeignKey('Bike', on_delete=models.CASCADE)
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



# user profile


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # Always ensure profile exists. If created => create profile.
    if created:
        Profile.objects.create(user=instance)
    else:
        # get_or_create is safe if profile missing
        Profile.objects.get_or_create(user=instance)


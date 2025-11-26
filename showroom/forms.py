from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import (
    TestRideBooking,
    ContactMessage,
    BikePurchase,
    Profile,
    Booking
)

# -----------------------------
#  Test Ride Booking Form
# -----------------------------
class TestRideBookingForm(forms.ModelForm):
    class Meta:
        model = TestRideBooking
        fields = ['customer_name', 'email', 'phone', 'preferred_date', 'message']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# -----------------------------
#  Contact Form
# -----------------------------
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

# -----------------------------
#  Bike Purchase Form
# -----------------------------
class BikePurchaseForm(forms.ModelForm):
    class Meta:
        model = BikePurchase
        fields = ['customer_name', 'email', 'phone', 'color', 'variant', 'address', 'payment_mode']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

# -----------------------------
#  User Registration Form
# -----------------------------
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# -----------------------------
#  Profile Update Form
# -----------------------------
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# -----------------------------
#  User Update Form
# -----------------------------
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

# -----------------------------
#  Bike Booking Form (NEW)
# -----------------------------
class BikeBookingForm(forms.ModelForm):
    # This is NOT part of the model
    pincode = forms.CharField(
        max_length=6,
        required=False,
        label="Pincode"
    )

    class Meta:
        model = Booking
        fields = [
            'customer_name',
            'email',
            'phone',
            'address',
            'city',
            'state',
            'booking_type',
            'preferred_date',
            'preferred_time'
        ]
        widgets = {
            'preferred_date': forms.DateInput(attrs={'type': 'date'}),
            'preferred_time': forms.TimeInput(attrs={'type': 'time'}),
        }

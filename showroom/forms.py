from django import forms
from .models import TestRideBooking
from .models import ContactMessage
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




class TestRideBookingForm(forms.ModelForm):
    class Meta:
        model = TestRideBooking
        fields = ['customer_name', 'email', 'phone', 'preferred_date', 'message']
        widgets = {
            'preferred_date': forms.DateInput(attrs={'type': 'date'}),
            'message': forms.Textarea(attrs={'rows': 3}),
        }




class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your Message'}),
        }

#booking
from .models import BikeBooking

class BikeBookingForm(forms.ModelForm):
    class Meta:
        model = BikeBooking
        fields = ['name', 'email', 'phone', 'bike_model', 'booking_date', 'message']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'message': forms.Textarea(attrs={'rows': 3}),
        }


from .models import BikePurchase

class BikePurchaseForm(forms.ModelForm):
    class Meta:
        model = BikePurchase
        fields = ['customer_name', 'email', 'phone', 'color', 'variant', 'address', 'payment_mode']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }



from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


# ✅ User Registration Form
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



# ✅ Profile Update Form (includes bio + picture)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# ✅ User Info Update Form (for username/email)
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

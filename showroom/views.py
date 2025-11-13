from django.shortcuts import render, redirect, get_object_or_404
from .models import Bike
from .forms import TestRideBookingForm
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

from django.contrib import messages
from .forms import BikeBookingForm


from .forms import BikePurchaseForm

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm
from .models import Profile
from django.contrib.auth.models import User


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required

from .models import Bike, Profile
from .forms import (
    TestRideBookingForm, ContactForm, BikeBookingForm,
    BikePurchaseForm, UserRegisterForm, ProfileUpdateForm, UserUpdateForm
)
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()



def home(request):
    bikes = Bike.objects.all()
    return render(request, 'showroom/home.html', {'bikes': bikes})


def bike_detail(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)
    return render(request, 'showroom/bike_detail.html', {'bike': bike})




def book_test_ride(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)

    if request.method == 'POST':
        form = TestRideBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.bike = bike
            booking.save()

            # ✉️ 1️⃣ Email to showroom owner
            admin_subject = f"New Test Ride Booking - {bike.name}"
            admin_message = f"""
New test ride booking received!

Customer Name: {booking.customer_name}
Email: {booking.email}
Phone: {booking.phone}
Preferred Date: {booking.preferred_date}

Bike: {bike.brand} - {bike.name}
Message: {booking.message or 'No additional message'}

Regards,
EV Showroom Website
            """
            send_mail(
                admin_subject,
                admin_message,
                settings.EMAIL_HOST_USER,
                ['prithvirajchouhan2003@gmail.com'],  # showroom owner email
                fail_silently=False,
            )

            # ✉️ 2️⃣ Confirmation email to the customer
            customer_subject = f"✅ Test Ride Confirmation - {bike.name}"
            customer_message = f"""
Hi {booking.customer_name},

Thank you for booking a test ride with EV Showroom! 🎉

Here are your booking details:
🏍️ Bike: {bike.brand} - {bike.name}
📅 Preferred Date: {booking.preferred_date}
📞 Phone: {booking.phone}

We’ll contact you soon to confirm your slot.
If you have any questions, feel free to reply to this email.

Best regards,  
EV Showroom Team ⚡
            """
            send_mail(
                customer_subject,
                customer_message,
                settings.EMAIL_HOST_USER,  # from
                [booking.email],           # to customer
                fail_silently=False,
            )

            return render(request, 'showroom/booking_success.html', {'bike': bike})
    else:
        form = TestRideBookingForm()

    return render(request, 'showroom/book_test_ride.html', {'form': form, 'bike': bike})


# for contact

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            # Send email notification to showroom owner
            subject = f"📩 New Contact Message: {contact.subject}"
            message = f"""
New inquiry received on EV Showroom!

Name: {contact.name}
Email: {contact.email}

Message:
{contact.message}
"""
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                ['prithvirajchouhan2003@gmail.com'],  # <-- Change this
                fail_silently=False,
            )

            return render(request, 'showroom/contact_success.html', {'contact': contact})
    else:
        form = ContactForm()

    return render(request, 'showroom/contact.html', {'form': form})

# about
def about_view(request):
    return render(request, "showroom/about.html")



def book_bike(request):
    if request.method == 'POST':
        form = BikeBookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your test ride booking has been submitted successfully!')
            return redirect('book_bike')
    else:
        form = BikeBookingForm()
    return render(request, 'book_bike.html', {'form': form})




def buy_bike(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)

    if request.method == "POST":
        form = BikePurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.bike = bike
            purchase.save()
            messages.success(request, f"Your order for {bike.name} has been placed successfully!")
            return redirect('thank_you')
    else:
        form = BikePurchaseForm()

    return render(request, 'showroom/buy_bike.html', {'bike': bike, 'form': form})


def thank_you(request):
    return render(request, 'showroom/thank_you.html')


# register login and logout

# showroom/views.py

# ---------- Auth views ----------
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.save()
            # Profile will be created by signal (see signals update). To be safe:
            Profile.objects.get_or_create(user=user)
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'showroom/register.html', {'form': form})

def login_view(request):
    # Accepts either username or email in the single field named 'identifier'
    if request.method == 'POST':
        identifier = request.POST.get('identifier')  # can be username or email
        password = request.POST.get('password')
        user = None

        # Try authenticate as username
        user = authenticate(request, username=identifier, password=password)
        if user is None:
            # Try treating identifier as email
            try:
                possible = User.objects.get(email__iexact=identifier)
            except User.DoesNotExist:
                possible = None
            if possible:
                user = authenticate(request, username=possible.username, password=password)

        if user:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'showroom/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'showroom/profile.html', {'profile': profile_obj})

@login_required
def edit_profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_obj)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '✅ Profile updated successfully!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile_obj)

    return render(request, 'showroom/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

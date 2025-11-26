from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

from .models import Bike, Profile, Booking
from .forms import (
    TestRideBookingForm,
    ContactForm,
    BikeBookingForm,
    BikePurchaseForm,
    UserRegisterForm,
    ProfileUpdateForm,
    UserUpdateForm,
    

)

User = get_user_model()


# ------------------ Home ------------------
def home(request):
    bikes = Bike.objects.all()
    return render(request, 'showroom/home.html', {'bikes': bikes})


def bike_detail(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)
    return render(request, 'showroom/bike_detail.html', {'bike': bike})


# ------------------ Test Ride Booking ------------------
@login_required
def book_test_ride(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)

    if request.method == 'POST':
        form = TestRideBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.bike = bike
            booking.user = request.user                  # <-- ADD THIS
            booking.email = request.user.email 
            booking.save()

            # Admin email
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
EV Showroom

"""

            send_mail(
                admin_subject, admin_message,
                settings.EMAIL_HOST_USER,
                ['prithvirajchouhan2003@gmail.com']
            )

            # Customer email
            customer_subject = f"Test Ride Confirmed - {bike.name}"
            customer_message = f"""
Hi {booking.customer_name},

Thanks you for booking a test ride with EV Showroom!🎉

Here are your booking details:
🏍️ Bike: {bike.brand} - {bike.name} 
📅 Preferred Date: {booking.preferred_date} 
📞 Phone: {booking.phone}

We’ll contact you soon to confirm your slot.
If you have any questions, feel free to reply to this email.

Thank you!
EV Showroom Team⚡

"""

            send_mail(
                customer_subject,
                customer_message,
                settings.EMAIL_HOST_USER,
                [booking.email]
            )

            return render(request, 'showroom/booking_success.html', {'bike': bike})

    else:
        form = TestRideBookingForm()

    return render(request, 'showroom/book_test_ride.html', {'form': form, 'bike': bike})


# ------------------ Contact ------------------
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            send_mail(
                f"New Message: {contact.subject}",
                contact.message,
                settings.EMAIL_HOST_USER,
                ['prithvirajchouhan2003@gmail.com']
            )

            return render(request, 'showroom/contact_success.html')

    else:
        form = ContactForm()

    return render(request, 'showroom/contact.html', {'form': form})


def about_view(request):
    return render(request, "showroom/about.html")


# ------------------ Buy Bike ------------------
def buy_bike(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)

    if request.method == "POST":
        form = BikePurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.bike = bike
            purchase.user = request.user                 # <-- ADD THIS
            purchase.email = request.user.email
            purchase.save()

            messages.success(request, f"Order for {bike.name} placed!")
            return redirect('thank_you')
    else:
        form = BikePurchaseForm()

    return render(request, 'showroom/buy_bike.html', {'bike': bike, 'form': form})


def thank_you(request):
    return render(request, 'showroom/thank_you.html')


# ------------------ Auth ------------------
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            messages.success(request, "Account created! Login now.")
            return redirect('login')

    else:
        form = UserRegisterForm()

    return render(request, 'showroom/register.html', {'form': form})


def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')

        user = authenticate(request, username=identifier, password=password)

        if user:
            login(request, user)
            return redirect(next_url or 'home')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'showroom/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')



from django.contrib.auth.decorators import login_required
from .models import Profile, TestRideBooking, BikePurchase, Booking
@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)

    bookings = Booking.objects.filter(email=request.user.email).order_by('-created_at')
    test_rides = TestRideBooking.objects.filter(email=request.user.email).order_by('-created_at')
    bike_purchases = BikePurchase.objects.filter(email=request.user.email).order_by('-date')

    return render(request, 'showroom/profile.html', {
        'profile': profile_obj,
        'test_rides': test_rides,
        'bike_purchases': bike_purchases,
        'bookings': bookings,
    })




@login_required
def edit_profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_obj)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated!")
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile_obj)

    return render(request, 'showroom/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
        
    })


# ------------------ NEW: Bike Booking ------------------
@login_required
def book_bike(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)

    if request.method == 'POST':
        form = BikeBookingForm(request.POST)

        if form.is_valid():
            preferred_date = form.cleaned_data['preferred_date']
            preferred_time = form.cleaned_data['preferred_time']

            # Optional: pincode (not saved in DB)
            pincode = form.cleaned_data.get('pincode')
            print("User entered pincode:", pincode)

            # Check for slot conflict
            slot_taken = Booking.objects.filter(
                bike=bike,
                preferred_date=preferred_date,
                preferred_time=preferred_time,
                status="confirmed"
            ).exists()

            if slot_taken:
                messages.error(
                    request,
                    "This time slot is already booked. Please choose another date/time."
                )
                # ❗ Do NOT redirect — keeps form data & errors on same page
                return render(request, "showroom/book_bike.html", {
                    'bike': bike,
                    'form': form
                })

            # Save booking (except pincode)
            booking = form.save(commit=False)
            booking.bike = bike
            
            booking.user = request.user                 # <-- ADD THIS
            booking.email = request.user.email          # <-- ADD THIS
            booking.status = "pending"
            booking.save()

            # Redirect to success page
            return redirect('booking_success', booking_id=booking.id)

        # Form is not valid → show errors on same page
        return render(request, "showroom/book_bike.html", {
            'bike': bike,
            'form': form
        })

    else:
        form = BikeBookingForm()

    return render(request, "showroom/book_bike.html", {
        'bike': bike,
        'form': form
    })



def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, "showroom/bookingBike_success.html", {'booking': booking})




# now we create a profile based view for profile mnagagement
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from .models import Booking, TestRideBooking, BikePurchase
@login_required
def view_booking(request, id):
    booking = get_object_or_404(Booking, id=id, user=request.user)
    return render(request, "showroom/view_booking.html", {"booking": booking})


@login_required
def cancel_booking(request, id):
    booking = get_object_or_404(Booking, id=id, user=request.user)

    if booking.status == "cancelled":
        messages.info(request, "Booking is already cancelled.")
    else:
        booking.status = "cancelled"
        booking.save()
        messages.success(request, "Your booking has been cancelled.")

    return redirect("profile")


@login_required
def view_test_ride(request, id):
    test_ride = get_object_or_404(TestRideBooking, id=id, user=request.user)
    return render(request, "showroom/view_test_ride.html", {"test_ride": test_ride})


@login_required
def cancel_test_ride(request, id):
    test_ride = get_object_or_404(TestRideBooking, id=id, user=request.user)
    test_ride.delete()
    messages.success(request, "Test ride request cancelled.")
    return redirect("profile")


@login_required
def view_purchase(request, id):
    purchase = get_object_or_404(BikePurchase, id=id, user=request.user)
    return render(request, "showroom/view_purchase.html", {"purchase": purchase})


@login_required
def invoice_download(request, id):
    purchase = get_object_or_404(BikePurchase, id=id, user=request.user)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=Invoice-{purchase.id}.pdf"

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 20)
    p.drawString(50, height - 50, "EV Showroom - Invoice")

    p.setFont("Helvetica", 12)
    p.drawString(50, height - 100, f"Invoice ID: {purchase.id}")
    p.drawString(50, height - 120, f"Customer: {purchase.user.get_full_name()}")
    p.drawString(50, height - 140, f"Bike: {purchase.bike.brand} {purchase.bike.name}")
    p.drawString(50, height - 160, f"Variant: {purchase.variant}")
    p.drawString(50, height - 180, f"Color: {purchase.color}")
    p.drawString(50, height - 200, f"Payment Mode: {purchase.payment_mode}")
    p.drawString(50, height - 220, f"Date: {purchase.date.strftime('%b %d, %Y')}")

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 260, "Thank you for your purchase!")

    p.showPage()
    p.save()
    return response


@login_required
def delete_purchase(request, id):
    purchase = get_object_or_404(BikePurchase, id=id, user=request.user)
    purchase.delete()
    messages.success(request, "Purchase record deleted successfully.")
    return redirect("profile")

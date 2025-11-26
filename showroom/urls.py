from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Bike Pages
    path('bike/<int:bike_id>/', views.bike_detail, name='bike_detail'),
    path('bike/<int:bike_id>/book/', views.book_test_ride, name='book_test_ride'),
    path("book/<int:bike_id>/", views.book_bike, name="book_bike"),

    # Booking Success Page
    path("booking-success/<int:booking_id>/", views.booking_success, name="booking_success"),


    # Buy Bike
    path('buy/<int:bike_id>/', views.buy_bike, name='buy_bike'),

    # Static Pages
    path("contact/", views.contact_view, name="contact"),
    path("about/", views.about_view, name="about"),

    # User Accounts
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Profile
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Thank You Page
    path('thank-you/', views.thank_you, name='thank_you'),


    path("booking/<int:id>/view/", views.view_booking, name="view_booking"),
    path("booking/<int:id>/cancel/", views.cancel_booking, name="cancel_booking"),

    path("test-ride/<int:id>/view/", views.view_test_ride, name="view_test_ride"),
    path("test-ride/<int:id>/cancel/", views.cancel_test_ride, name="cancel_test_ride"),

    path("purchase/<int:id>/view/", views.view_purchase, name="view_purchase"),
    path("purchase/<int:id>/invoice/", views.invoice_download, name="invoice_download"),
    path("purchase/<int:id>/delete/", views.delete_purchase, name="delete_purchase"),


]

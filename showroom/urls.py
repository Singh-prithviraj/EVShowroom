from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bike/<int:bike_id>/', views.bike_detail, name='bike_detail'),  # 👈 new
    path('bike/<int:bike_id>/book/', views.book_test_ride, name='book_test_ride'),
    path("contact/", views.contact_view, name="contact"),
    path("about/", views.about_view, name="about"),
    path('book/', views.book_bike, name='book_bike'),
    path('buy/<int:bike_id>/', views.buy_bike, name='buy_bike'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),          # lowercase!
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]




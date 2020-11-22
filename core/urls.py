from django.contrib import admin
from django.urls import path

from charity_donation.views import AddDonationView, LandingPageView, LoginView, LogoutView, \
    RegisterView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', LandingPageView.as_view(), name='landing_page'),
    path('add-donation/', AddDonationView.as_view(), name='add_donation'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]

from django.shortcuts import render
from django.views import View


class LandingPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charity_donation/index.html', {})


class AddDonationView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charity_donation/form.html', {})
        # return render(request, 'charity_donation/form-confirmation.html', {})


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charity_donation/login.html', {})


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charity_donation/register.html', {})

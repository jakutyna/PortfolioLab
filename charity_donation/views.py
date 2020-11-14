from django.db.models import Sum
from django.shortcuts import render
from django.views import View

from .models import Donation, Institution


class LandingPageView(View):
    def get(self, request, *args, **kwargs):
        donations = Donation.objects.all()
        institutions = Institution.objects.all()
        bags_number = donations.aggregate(Sum('quantity'))['quantity__sum']

        institutions_number = len(list(dict.fromkeys([donation.institution for donation in donations])))

        ctx = {
            "bags_num": 0 if bags_number is None else bags_number,
            "institutions_num": institutions_number,
            "institutions": institutions,
        }
        return render(request, 'charity_donation/index.html', ctx)


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

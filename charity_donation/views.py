from django.contrib.auth import views as auth_views, get_user_model
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView

from .forms import LoginForm, RegisterForm
from .models import CustomUser, Donation, Institution


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


class LoginView(auth_views.LoginView):
    authentication_form = LoginForm
    redirect_authenticated_user = True
    template_name = 'charity_donation/login.html'

    # def get(self, request, *args, **kwargs):
    #     return render(request, 'charity_donation/login.html', {})

    def form_invalid(self, form):
        """
        Sets behaviour for invalid form.

        If user with given email does not exist redirect to registration page.
        If password is invalid, render the invalid form.
        """
        username = form.cleaned_data['username']
        UserModel = get_user_model()

        try:
            UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return redirect('register')
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(auth_views.LogoutView):
    pass


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'charity_donation/register.html'
    success_url = reverse_lazy('login')

    # def get(self, request, *args, **kwargs):
    #     return render(request, 'charity_donation/register.html', {})

from django.contrib.auth import views as auth_views, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView

from .forms import DonationForm, IsTakenForm, LoginForm, RegisterForm
from .models import Donation, Institution


class LandingPageView(View):
    def get(self, request, *args, **kwargs):
        donations = Donation.objects.all()
        institutions = Institution.objects.all()
        bags_number = donations.aggregate(Sum('quantity'))['quantity__sum']

        # Only institutions to which donations were made are listed
        institutions_number = len(list(dict.fromkeys([donation.institution for donation in donations])))

        ctx = {
            "bags_num": 0 if bags_number is None else bags_number,
            "institutions_num": institutions_number,
            "institutions": institutions,
        }
        return render(request, 'charity_donation/index.html', ctx)


class AddDonationView(LoginRequiredMixin, CreateView):
    template_name = 'charity_donation/add_donation.html'
    form_class = DonationForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user  # Fill user field in model instance
        self.object.save()
        form.save_m2m()
        return render(self.request, 'charity_donation/donation_confirmation.html',
                      self.get_context_data())  # Render form confirmation


class LoginView(auth_views.LoginView):
    authentication_form = LoginForm
    redirect_authenticated_user = True
    template_name = 'charity_donation/login.html'

    def form_invalid(self, form):
        """
        Sets behaviour for invalid form.

        If user with given email does not exist redirect to registration page.
        If password is invalid, render the invalid form.
        """
        username = self.request.POST['email']
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


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        donations = Donation.objects.filter(user=request.user).order_by('is_taken', '-pick_up_date')
        form = IsTakenForm(queryset=donations)

        form_and_donations = [{'is_taken': form['is_taken'][idx], 'donation': donation}
                              for idx, donation in enumerate(donations)]
        # for idx, donation in enumerate(donations):
        #     donations_and_form.append({'is_taken': })
        ctx = {
            'form': form,
            'donations': donations,
            'form_and_donations': form_and_donations
        }
        return render(request, 'charity_donation/user_profile.html', ctx)

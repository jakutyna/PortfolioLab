from random import choice
from string import ascii_letters

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from .models import Category, Donation, Institution


class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        """Extends ModelChoiceField labels TODO: explain further."""
        return "{}<br> {}".format(obj, obj.description)


class CustomDateInput(forms.DateInput):
    """
    Modified input type for date inputs in forms (from default 'text' type).

    For nicer displaying of date field in browser.
    """
    input_type = 'date'


class CustomTimeInput(forms.DateInput):
    """
    Modified input type for time inputs in forms (from default 'text' type).

    For nicer displaying of time field in browser.
    """
    input_type = 'time'


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Imię'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Nazwisko'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Hasło'
        self.fields['password2'].widget.attrs['placeholder'] = 'Powtórz hasło'
        self.fields['first_name'].widget.attrs['required'] = True

    def save(self, commit=True):
        """
        Modified UserCreationForm save method.

        Creates username based on first 5 letters of email local-part and 25 random letters
        (username is not used for authentication in this project but is required by User model).
        """

        email_local_part = self.cleaned_data['email'].split('@')[0]
        username_start = email_local_part[:5] if len(email_local_part) >= 5 else email_local_part
        self.instance.username = username_start + ''.join(
            [choice(ascii_letters) for _ in range(30 - len(username_start))])

        return super(RegisterForm, self).save(commit=commit)


class LoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Email'}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['password'].widget.attrs['placeholder'] = 'Hasło'
        self.error_messages['invalid_login'] = 'Podaj poprawny email i hasło.'

    def clean(self):
        # Username for authentication replaced with email.
        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ('quantity', 'address', 'phone_number', 'city', 'zip_code', 'pick_up_date',
                  'pick_up_time', 'pick_up_comment', 'categories', 'institution')
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1, 'step': 1}),
            # 'pick_up_date': CustomDateInput(),
            # 'pick_up_time': CustomTimeInput(),
            'pick_up_comment': forms.Textarea(attrs={'rows': 5, 'cols': 20}),
        }

    def __init__(self, *args, **kwargs):
        super(DonationForm, self).__init__(*args, **kwargs)

        self.fields['categories'] = \
            forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                           widget=forms.CheckboxSelectMultiple)

        self.fields['institution'] = \
            CustomModelChoiceField(queryset=Institution.objects.all(),
                                   widget=forms.RadioSelect, empty_label=None)


class IsTakenForm(forms.Form):
    """
    Form for setting 'is_taken' field of 'Donation' model
    (form used in 'UserProfileView).
    """

    def __init__(self, queryset, *args, **kwargs):
        super(IsTakenForm, self).__init__(*args, **kwargs)

        # ModelMultipleChoiceField used instead of BooleanField
        # to be able to set 'is_taken' field for multiple Donation instances at once.
        self.fields['is_taken'] = forms.ModelMultipleChoiceField(queryset=queryset,
                                                                 widget=forms.CheckboxSelectMultiple)

        self.fields['is_taken'].initial = queryset.filter(is_taken=True).values_list('id', flat=True)

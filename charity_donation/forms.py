from random import choice
from string import ascii_letters

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    # TODO: Duplicate email message + error display in templates

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Imię'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Nazwisko'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Hasło'
        self.fields['password2'].widget.attrs['placeholder'] = 'Powtórz hasło'

        self.fields['first_name'].widget.attrs['required'] = True

        for fieldname in self.fields:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].label = ''

    def save(self, commit=True):
        """
        Modified UserCreationForm save method

        Creates username based on first 5 letters of email local-part and 25 random letters
        """

        email_local_part = self.cleaned_data['email'].split('@')[0]
        username_start = email_local_part[:5] if len(email_local_part) >= 5 else email_local_part
        self.instance.username = username_start + ''.join(
            [choice(ascii_letters) for _ in range(30 - len(username_start))])

        return super(RegisterForm, self).save(commit=commit)


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.error_messages['invalid_login'] = 'Podaj poprawny email i hasło.'
        self.fields['username'].widget.attrs['placeholder'] = 'Email'
        self.fields['password'].widget.attrs['placeholder'] = 'Hasło'
        for fieldname in self.fields:
            self.fields[fieldname].label = ''

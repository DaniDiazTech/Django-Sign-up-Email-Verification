from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.template.loader import render_to_string

from .token import token_generator

user_model = get_user_model()

# Sign Up Form
class SignUpForm(UserCreationForm):

    email = forms.EmailField(
        max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = user_model
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

    # We need the user object, so it's an additional parameter
    def send_activation_email(self, request, user):
        current_site = get_current_site(request)
        subject = 'Activate Your Account'
        message = render_to_string(
            'users/activate_account.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user),
            }
        )

        user.email_user(subject, message, html_message=message)

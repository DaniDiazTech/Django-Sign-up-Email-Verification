from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, RedirectView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView

from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text

from .forms import SignUpForm, token_generator, user_model


# Create your views here.
class SignUpView(CreateView):
    form_class = SignUpForm 
    template_name = 'users/signup.html'
    success_url = reverse_lazy('check_email')

    def form_valid(self, form):
        to_return = super().form_valid(form)
        
        user = form.save()
        user.is_active = False # Turns the user status to inactive
        user.save()

        form.send_activation_email(self.request, user)

        return to_return


class ActivateView(RedirectView):

    url = reverse_lazy('success')

    # Custom get method
    def get(self, request, uidb64, token):

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = user_model.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return super().get(request, uidb64, token)
        else:
            return render(request, 'users/activate_account_invalid.html')

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
class CheckEmailView(TemplateView):
    template_name = 'users/check_email.html'

class SuccessView(TemplateView):
    template_name = 'users/success.html'

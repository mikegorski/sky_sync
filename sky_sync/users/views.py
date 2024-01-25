from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, UserPasswordChangeForm, UserAuthenticationForm
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.views.generic import TemplateView  ##################################################################
from .utils import get_email_message
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.http.response import HttpResponseNotFound, HttpResponseBadRequest
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str


class CustomLoginView(LoginView):
    form_class = UserAuthenticationForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super().form_valid(form)


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('confirm-registration')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        activation_msg = get_email_message(
            recipient_email=user.email,
            subject="Activate Your SkySync Account",
            html_template_name='users/acc_activation_email.html',
            user=user,
            domain=get_current_site(self.request).domain,
        )
        activation_msg.send()

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to create an account.")
        return super().form_invalid(form)


class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = 'users/reset_password.html'
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        username = self.request.user.username
        messages.success(self.request, f"Password for {username} has been changed.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to change the password.")
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class HomeView(TemplateView):
    template_name = 'users/home.html'  # Default template

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            self.template_name = 'users/landing_page.html'
        return render(request, self.template_name)


class LandingView(TemplateView):
    template_name = 'users/landing_page.html'  # Default template

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.template_name = 'users/home.html'
        return render(request, self.template_name)


class AboutView(TemplateView):
    template_name = 'users/about.html'


class AfterRegistrationView(TemplateView):
    template_name = 'users/after_registration.html'


class ActivationView(TemplateView):
    def get(self, request, *args, **kwargs):
        uidb64 = kwargs["uidb64"]
        token = kwargs["token"]
        uid = force_str(urlsafe_base64_decode(uidb64))
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return HttpResponseNotFound("User not found.")
        if not default_token_generator.check_token(user, token):
            return HttpResponseBadRequest("Invalid token.")
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated successfully and you can now sign in.")
        return redirect('login')

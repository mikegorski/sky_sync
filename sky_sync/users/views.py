from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, UserPasswordChangeForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(self.request, f"Account for {username} has been created.")
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


def home(request):
    return render(request, 'users/home.html')

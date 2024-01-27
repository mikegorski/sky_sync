from django.urls import path, include, re_path
from django.contrib.auth.views import LogoutView
from .views import (
    RegisterView,
    CustomLoginView,
    AboutView,
    ActivationView,
    AfterRegistrationView,
    LandingView,
    HomeView,
)

urlpatterns = [
    path('', LandingView.as_view(), name='landing-page'),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
    path('home/', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('confirm-registration/', AfterRegistrationView.as_view(), name='confirm-registration'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('activate/<str:uidb64>/<str:token>', ActivationView.as_view(), name='activate-account'),
    # path("password_reset", PasswordResetRequestView.as_view(), name="password_reset"),
    # path(
    #     "password_reset/done/",
    #     PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
    #     name="password_reset_done",
    # ),
    # path(
    #     "reset/<uidb64>/<token>/",
    #     PasswordResetConfirmView.as_view(
    #         template_name="users/password_reset_confirm.html"
    #     ),
    #     name="password_reset_confirm",
    # ),
    # path(
    #     "reset/complete/",
    #     PasswordResetCompleteView.as_view(
    #         template_name="users/password_reset_complete.html"
    #     ),
    #     name="password_reset_complete",
    # ),
]

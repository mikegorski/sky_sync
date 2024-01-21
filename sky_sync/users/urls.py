from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    landing_page,
    RegisterView,
    ChangePasswordView,
    CustomLoginView,
    activation_view,
    home_view,
    after_registration_view,
    about_view,
)

urlpatterns = [
    path('', landing_page, name='landing-page'),
    path('home/', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('confirm-registration/', after_registration_view, name='confirm-registration'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('activate/<str:uidb64>/<str:token>', activation_view, name='activate-account')
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

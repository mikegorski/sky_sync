from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    last_failed_login_attempt = models.DateTimeField(null=True, default=None)
    last_login = models.DateTimeField(null=True, default=None)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=True, default=None)

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    last_failed_login_attempt = models.DateTimeField(null=True, default=None)
    is_active = models.BooleanField(default=False)

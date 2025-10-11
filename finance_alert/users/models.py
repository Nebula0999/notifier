from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Inherit username, email, first_name, last_name, password, is_active, etc.
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

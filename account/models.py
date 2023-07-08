from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    # fields: username, password, first_name, last_name, email, address, phone_number

    address = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=12)

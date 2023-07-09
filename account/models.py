from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from account.manager import UserManager


# Create your models here.

class CustomUser(AbstractBaseUser):
    # fields: phone_number, email, password, full_name, email, address
    full_name = models.CharField(max_length=40, null=True, blank=False)
    email = models.EmailField(max_length=100, unique=True, blank=False)
    address = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=12, unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ('email', )

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

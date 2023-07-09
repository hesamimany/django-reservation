from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from .models import CustomUser


class PhoneBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, password=None):
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            if user.check_password(password) and (user.is_admin or user.is_staff):
                return user
        except CustomUser.DoesNotExist:
            return None


    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None

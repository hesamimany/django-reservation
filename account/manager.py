from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, password):
        if not email:
            raise ValueError("No Email")

        if not phone_number:
            raise ValueError("No phone number")

        user = get_user_model()(
            email=self.normalize_email(email),
            phone_number=phone_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, password):
        user = self.create_user(phone_number, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

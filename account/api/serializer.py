from django.contrib.auth import get_user_model
from rest_framework import serializers
from account.models import CustomUser
from django.contrib.auth.hashers import make_password


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['phone_number', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        email = validated_data['email']
        password = validated_data['password']

        user = CustomUser.objects.create_user(
            phone_number=phone_number,
            email=email,
            password=password,
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

from rest_framework import serializers
from account.models import CustomUser
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'address', 'password', 'phone_number', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        address = validated_data['address']
        email = validated_data['email']
        phone_number = validated_data['phone_number']

        user = CustomUser.objects.create(
            username=username,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone_number=phone_number,
            email=email,
        )

        return user

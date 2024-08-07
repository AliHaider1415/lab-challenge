from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model

from .models import Profile
import re


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    ethereum_addr = serializers.CharField(max_length=250, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "password", "password2", "ethereum_addr")
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True},
        }

    def validate_ethereum_addr(self, value):
        
        if not re.match(r'^0x[a-fA-F0-9]{40}$', value):
            raise serializers.ValidationError("Invalid Ethereum address format. Ensure it starts with '0x' and is followed by 40 hexadecimal characters.")
        
        return value

    def save(self, **kwargs):
        user = get_user_model()(
            email=self.validated_data["email"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
        )

        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords do not match!"})

        user.set_password(password)
        user.save()

        ethereum_addr = self.validated_data["ethereum_addr"]
        Profile.objects.create(user=user, ethereum_addr=ethereum_addr)

        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "is_staff", "first_name", "last_name")

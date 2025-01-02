from rest_framework.serializers import Serializer, CharField, EmailField
from rest_framework.exceptions import ValidationError
import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Call parent validation
        data = super().validate(attrs)
        
        # Access the authenticated user
        user = self.user
        
        # Add additional user details to the response
        data["id"] = user.id
        data["username"] = user.username
        data["email"] = user.email
        return data



class UserRegistrationSerializer(Serializer):
    first_name = CharField(max_length=150, write_only=True)
    last_name = CharField(max_length=150, write_only=True)
    email = EmailField(write_only=True)
    password1 = CharField(max_length=150, write_only=True)
    password2 = CharField(max_length=150, write_only=True)

    def validate_password1(self, value):
        if len(value) < 6:
            raise ValidationError("Password must have at least 6 characters.")
        if not re.search(r"\d", value):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r"[A-Z]", value):
            raise ValidationError(
                "Password must contain at least one uppercase letter."
            )
        if not re.search(r"[a-z]", value):
            raise ValidationError(
                "Password must contain at least one lowercase letter."
            )
        return value

    def validate(self, attrs):
        if CustomUser.objects.filter(email=attrs["email"]).exists():
            raise ValidationError({"email": "Email already taken"})

        if attrs["password1"] != attrs["password2"]:
            raise ValidationError({"password2": "Password do not match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        pasword = validated_data.pop("password1")
        username = f"{validated_data['first_name']} {validated_data['last_name']}"

        user = CustomUser.objects.create_user(
            **validated_data, password=pasword, username=username
        )

        return user

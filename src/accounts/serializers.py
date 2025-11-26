from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=False) 

    class Meta:
        model = User
        fields  = ("email", "username", "password")

    def create(self, validated_data):
        email = validated_data["email"]
        username = validated_data.get("username")
        
        if not username:
            username = email.split("@")[0]

        user = User.objects.create_user(
            email=email,
            username=username,
            password=validated_data["password"]
        )
        return user
    
    def validate_password(self, value):
        validate_password(value)
        return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "username", "created_at")
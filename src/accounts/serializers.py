from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = User
        fields = ("id", "email", "username", "password")

    def validate(self, attrs):
        username = attrs.get("username")
        email = attrs.get("email")
        
        if not username and email:
            username = email.split("@")[0]
            
            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError({"username": "Username taken. Please provide a custom username."})
            attrs['username'] = username
            
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "username", "created_at")
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields  = ("email", "username", "password")

    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data.get("username") or validated_data["email"].split("@")[0],
            password=validated_data["password"]
        )
        return user
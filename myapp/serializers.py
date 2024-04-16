from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Friendship


User = get_user_model()


# Serializer for creating a new user
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "name", "Gender", "phonenumber")
        extra_kwargs = {"password": {"write_only": True}}
    
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# Serializer for user login
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


# Serializer for serializing friend requests
class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ["to_user"]


# Serializer for serializing friend requests from the perspective of the sender
class FriendshipSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ["from_user"]


# Serializer for accepting friend requests
class FriendRequestAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ["accepted"]

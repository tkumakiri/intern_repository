from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers

from .models import User, Follow, Dm, Good


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile', 'password')

    def create(self, validated_data):
        return User.objects.create_user(request_data=validated_data)

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile', 'password')

    def create(self, validated_data):
        return User.objects.create_user(request_data=validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        else:
            instance = super().update(instance, validated_data)
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'profile')

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('user', 'follow')

class DmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dm
        fields = ('text', 'sender', 'sent_at', 'receiver')

class GoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Good
        fields = ('post', 'user')

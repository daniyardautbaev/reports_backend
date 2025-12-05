from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Report

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        # create_user сам захеширует пароль
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
        )
        user.role = User.Roles.STAFF  # по умолчанию staff
        user.save()
        return user


class ReportSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Report
        fields = ('id', 'category', 'message', 'author', 'created_at')

    def validate_message(self, value):
        if not value.strip():
            raise serializers.ValidationError('message не может быть пустым')
        return value


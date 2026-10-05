# -*- coding: utf-8 -*-
"""Serializers for user registration and profile APIs."""

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "date_joined"]
        read_only_fields = ["id", "username", "date_joined"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password", "password_confirm"]

    def validate_username(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("نام کاربری الزامی است.")
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("این نام کاربری قبلاً ثبت شده است.")
        return value

    def validate(self, attrs):
        password_confirm = attrs.pop("password_confirm")
        if attrs["password"] != password_confirm:
            raise serializers.ValidationError({"password_confirm": "تکرار رمز عبور یکسان نیست."})
        validate_password(attrs["password"])
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

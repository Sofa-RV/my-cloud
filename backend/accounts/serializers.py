import re

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


USERNAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9]{3,19}$")


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        trim_whitespace=False,
    )

    class Meta:
        model = User
        fields = (
            "username",
            "full_name",
            "email",
            "password",
        )

    def validate_username(self, value):
        if not USERNAME_PATTERN.fullmatch(value):
            raise serializers.ValidationError(
                "Логин должен содержать от 4 до 20 символов, "
                "начинаться с латинской буквы и содержать только "
                "латинские буквы и цифры."
            )

        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким логином уже существует."
            )

        return value

    def validate_full_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Полное имя не должно быть пустым."
            )

        return value

    def validate_email(self, value):
        value = value.strip().lower()

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует."
            )

        return value

    def validate_password(self, value):
        if not re.search(r"[A-ZА-ЯЁ]", value):
            raise serializers.ValidationError(
                "Пароль должен содержать хотя бы одну заглавную букву."
            )

        if not re.search(r"\d", value):
            raise serializers.ValidationError(
                "Пароль должен содержать хотя бы одну цифру."
            )

        if not re.search(r"[^A-Za-zА-Яа-яЁё0-9]", value):
            raise serializers.ValidationError(
                "Пароль должен содержать хотя бы один специальный символ."
            )

        validate_password(value)

        return value

    def create(self, validated_data):
        password = validated_data.pop("password")

        return User.objects.create_user(
            password=password,
            **validated_data,
        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=20,
        trim_whitespace=True,
    )

    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate(self, attrs):
        user = User.objects.filter(
            username__iexact=attrs["username"],
        ).first()

        if user is None:
            raise serializers.ValidationError(
                "Неверный логин или пароль."
            )

        authenticated_user = user.check_password(
            attrs["password"],
        )

        if not authenticated_user:
            raise serializers.ValidationError(
                "Неверный логин или пароль."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "Учётная запись отключена."
            )

        attrs["user"] = user

        return attrs


class UserSerializer(serializers.ModelSerializer):
    files_count = serializers.IntegerField(read_only=True)
    files_size = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "full_name",
            "email",
            "is_app_admin",
            "is_active",
            "date_joined",
            "files_count",
            "files_size",
        )
        read_only_fields = (
            "id",
            "date_joined",
            "files_count",
            "files_size",
        )


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "full_name",
            "email",
            "is_app_admin",
        )
        read_only_fields = fields
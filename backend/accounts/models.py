import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


USERNAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9]{3,19}$")


def validate_username_format(value):
    if not USERNAME_PATTERN.fullmatch(value):
        raise ValidationError(
            "Логин должен содержать от 4 до 20 символов, "
            "начинаться с латинской буквы и содержать только "
            "латинские буквы и цифры."
        )


class User(AbstractUser):
    username = models.CharField(
        "логин",
        max_length=20,
        unique=True,
        validators=[validate_username_format],
    )

    full_name = models.CharField(
        "полное имя",
        max_length=150,
    )

    email = models.EmailField(
        "email",
        unique=True,
    )

    is_app_admin = models.BooleanField(
        "администратор приложения",
        default=False,
    )

    class Meta:
        ordering = ["username"]
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.username
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "full_name",
        "email",
        "is_app_admin",
        "is_staff",
        "is_active",
        "date_joined",
    )

    list_filter = (
        "is_app_admin",
        "is_staff",
        "is_active",
        "date_joined",
    )

    search_fields = (
        "username",
        "full_name",
        "email",
    )

    ordering = ("username",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                ),
            },
        ),
        (
            "Персональные данные",
            {
                "fields": (
                    "full_name",
                    "email",
                ),
            },
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_app_admin",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Важные даты",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "full_name",
                    "email",
                    "password1",
                    "password2",
                    "is_app_admin",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )
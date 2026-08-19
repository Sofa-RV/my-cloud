from rest_framework.permissions import BasePermission


class IsAppAdmin(BasePermission):
    message = "Требуются права администратора приложения."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_app_admin
        )
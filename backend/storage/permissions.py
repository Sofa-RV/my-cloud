from rest_framework.permissions import BasePermission


class IsFileOwnerOrAppAdmin(BasePermission):
    message = "Нет доступа к этому файлу."

    def has_object_permission(self, request, view, obj):
        return (
            obj.owner_id == request.user.id
            or request.user.is_app_admin
        )
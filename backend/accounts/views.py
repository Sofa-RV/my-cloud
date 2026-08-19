import logging

from django.contrib.auth import login
from django.contrib.auth import logout
from django.db.models import Count
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .permissions import IsAppAdmin
from .serializers import CurrentUserSerializer
from .serializers import LoginSerializer
from .serializers import RegistrationSerializer
from .serializers import UserSerializer


logger = logging.getLogger(__name__)


@ensure_csrf_cookie
def csrf_cookie_view(request):
    return JsonResponse(
        {
            "detail": "CSRF cookie установлена.",
        },
        status=200,
    )


class RegisterView(APIView):
    permission_classes = [AllowAny]

    serializer_class = RegistrationSerializer

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(
            *args,
            **kwargs,
        )

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = serializer.save()

        logger.info(
            "Зарегистрирован пользователь username=%s",
            user.username,
        )

        return Response(
            {
                "message": (
                    "Регистрация успешно завершена."
                ),
                "user": CurrentUserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    serializer_class = LoginSerializer

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(
            *args,
            **kwargs,
        )

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = serializer.validated_data["user"]

        login(request, user)

        logger.info(
            "Пользователь вошёл в систему username=%s",
            user.username,
        )

        return Response(
            {
                "message": "Вход выполнен успешно.",
                "user": CurrentUserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.user.username

        logout(request)

        logger.info(
            "Пользователь вышел из системы username=%s",
            username,
        )

        return Response(
            {
                "message": "Выход выполнен успешно.",
            },
            status=status.HTTP_200_OK,
        )


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            CurrentUserSerializer(
                request.user,
            ).data,
            status=status.HTTP_200_OK,
        )


class UserListView(APIView):
    permission_classes = [IsAppAdmin]

    def get(self, request):
        users = (
            User.objects
            .annotate(
                files_count=Count(
                    "stored_files",
                ),
                files_size=Sum(
                    "stored_files__size",
                ),
            )
            .order_by("username")
        )

        serializer = UserSerializer(
            users,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class UserDeleteView(APIView):
    permission_classes = [IsAppAdmin]

    def delete(self, request, user_id):
        if request.user.id == user_id:
            return Response(
                {
                    "detail": (
                        "Нельзя удалить текущего "
                        "администратора через этот API."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(
                id=user_id,
            )
        except User.DoesNotExist:
            return Response(
                {
                    "detail": "Пользователь не найден.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        username = user.username

        user.delete()

        logger.warning(
            "Администратор удалил пользователя "
            "username=%s admin=%s",
            username,
            request.user.username,
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class UserAdminFlagView(APIView):
    permission_classes = [IsAppAdmin]

    def patch(self, request, user_id):
        try:
            user = User.objects.get(
                id=user_id,
            )
        except User.DoesNotExist:
            return Response(
                {
                    "detail": "Пользователь не найден.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if user.id == request.user.id:
            return Response(
                {
                    "detail": (
                        "Нельзя изменить собственный "
                        "признак администратора."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.is_app_admin = not user.is_app_admin

        user.save(
            update_fields=[
                "is_app_admin",
            ],
        )

        logger.warning(
            "Изменён признак администратора "
            "username=%s is_app_admin=%s by=%s",
            user.username,
            user.is_app_admin,
            request.user.username,
        )

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_200_OK,
        )
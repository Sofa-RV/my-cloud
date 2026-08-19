from django.urls import path

from .views import CurrentUserView
from .views import LoginView
from .views import LogoutView
from .views import RegisterView
from .views import UserAdminFlagView
from .views import UserDeleteView
from .views import UserListView
from .views import csrf_cookie_view


urlpatterns = [
    path(
        "csrf/",
        csrf_cookie_view,
        name="csrf-cookie",
    ),
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path(
        "me/",
        CurrentUserView.as_view(),
        name="current-user",
    ),
    path(
        "users/",
        UserListView.as_view(),
        name="user-list",
    ),
    path(
        "users/<int:user_id>/",
        UserDeleteView.as_view(),
        name="user-delete",
    ),
    path(
        "users/<int:user_id>/admin/",
        UserAdminFlagView.as_view(),
        name="user-admin-flag",
    ),
]
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class AccountsApiTests(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.me_url = reverse("current-user")
        self.users_url = reverse("user-list")

        self.admin = User.objects.create_user(
            username="admin",
            full_name="Главный администратор",
            email="admin@example.com",
            password="AdminPassword1!",
            is_app_admin=True,
            is_staff=True,
        )

        self.user = User.objects.create_user(
            username="testuser",
            full_name="Тестовый пользователь",
            email="testuser@example.com",
            password="TestPassword1!",
        )

    def test_register_user(self):
        response = self.client.post(
            self.register_url,
            {
                "username": "newuser",
                "full_name": "Новый пользователь",
                "email": "newuser@example.com",
                "password": "NewPassword1!",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            User.objects.filter(
                username="newuser",
            ).exists(),
        )

    def test_register_rejects_invalid_username(self):
        response = self.client.post(
            self.register_url,
            {
                "username": "123-invalid",
                "full_name": "Неверный пользователь",
                "email": "invalid@example.com",
                "password": "ValidPassword1!",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_register_rejects_invalid_password(self):
        response = self.client.post(
            self.register_url,
            {
                "username": "passworduser",
                "full_name": "Пользователь",
                "email": "password@example.com",
                "password": "weakpass",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_login_creates_session(self):
        response = self.client.post(
            self.login_url,
            {
                "username": "testuser",
                "password": "TestPassword1!",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        me_response = self.client.get(self.me_url)

        self.assertEqual(
            me_response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            me_response.data["username"],
            "testuser",
        )

    def test_login_rejects_wrong_password(self):
        response = self.client.post(
            self.login_url,
            {
                "username": "testuser",
                "password": "WrongPassword1!",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_unauthenticated_user_cannot_open_me(self):
        response = self.client.get(self.me_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_logout_clears_session(self):
        self.client.login(
            username="testuser",
            password="TestPassword1!",
        )

        response = self.client.post(
            self.logout_url,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        me_response = self.client.get(self.me_url)

        self.assertEqual(
            me_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_only_app_admin_can_get_users(self):
        self.client.force_authenticate(
            user=self.user,
        )

        response = self.client.get(self.users_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.client.force_authenticate(
            user=self.admin,
        )

        response = self.client.get(self.users_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        usernames = {
            item["username"]
            for item in response.data
        }

        self.assertIn("admin", usernames)
        self.assertIn("testuser", usernames)

    def test_admin_can_toggle_admin_flag(self):
        self.client.force_authenticate(
            user=self.admin,
        )

        url = reverse(
            "user-admin-flag",
            kwargs={"user_id": self.user.id},
        )

        response = self.client.patch(
            url,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.user.refresh_from_db()

        self.assertTrue(
            self.user.is_app_admin,
        )

    def test_admin_cannot_toggle_own_admin_flag(self):
        self.client.force_authenticate(
            user=self.admin,
        )

        url = reverse(
            "user-admin-flag",
            kwargs={"user_id": self.admin.id},
        )

        response = self.client.patch(
            url,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_admin_can_delete_other_user(self):
        self.client.force_authenticate(
            user=self.admin,
        )

        url = reverse(
            "user-delete",
            kwargs={"user_id": self.user.id},
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            User.objects.filter(
                id=self.user.id,
            ).exists(),
        )

    def test_admin_cannot_delete_self(self):
        self.client.force_authenticate(
            user=self.admin,
        )

        url = reverse(
            "user-delete",
            kwargs={"user_id": self.admin.id},
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
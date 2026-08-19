import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User

from .models import StoredFile


TEST_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class StorageApiTests(APITestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(
            TEST_MEDIA_ROOT,
            ignore_errors=True,
        )

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            full_name="Тестовый пользователь",
            email="testuser@example.com",
            password="TestPassword1!",
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            full_name="Другой пользователь",
            email="otheruser@example.com",
            password="OtherPassword1!",
        )

        self.admin = User.objects.create_user(
            username="admin",
            full_name="Администратор",
            email="admin@example.com",
            password="AdminPassword1!",
            is_app_admin=True,
            is_staff=True,
        )

        self.file_list_url = reverse("file-list")
        self.file_upload_url = reverse("file-upload")

    def create_uploaded_file(self):
        return SimpleUploadedFile(
            name="test.txt",
            content=b"Test file content",
            content_type="text/plain",
        )

    def upload_file_as_user(self, user):
        self.client.force_authenticate(
            user=user,
        )

        response = self.client.post(
            self.file_upload_url,
            {
                "file": self.create_uploaded_file(),
                "comment": "Тестовый комментарий",
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        return StoredFile.objects.get(
            id=response.data["id"],
        )

    def test_unauthenticated_user_cannot_get_file_list(self):
        response = self.client.get(
            self.file_list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_user_can_upload_file(self):
        stored_file = self.upload_file_as_user(
            self.user,
        )

        self.assertEqual(
            stored_file.owner_id,
            self.user.id,
        )

        self.assertEqual(
            stored_file.original_name,
            "test.txt",
        )

        self.assertEqual(
            stored_file.size,
            len(b"Test file content"),
        )

        self.assertTrue(
            stored_file.file.name.startswith(
                f"users/{self.user.id}/",
            ),
        )

        self.assertTrue(
            stored_file.file.storage.exists(
                stored_file.file.name,
            ),
        )

    def test_user_sees_only_own_files(self):
        user_file = self.upload_file_as_user(
            self.user,
        )

        self.upload_file_as_user(
            self.other_user,
        )

        self.client.force_authenticate(
            user=self.user,
        )

        response = self.client.get(
            self.file_list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        file_ids = {
            item["id"]
            for item in response.data
        }

        self.assertEqual(
            file_ids,
            {user_file.id},
        )

    def test_admin_can_get_another_users_files(self):
        user_file = self.upload_file_as_user(
            self.user,
        )

        self.client.force_authenticate(
            user=self.admin,
        )

        response = self.client.get(
            self.file_list_url,
            {
                "owner_id": self.user.id,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data[0]["id"],
            user_file.id,
        )

    def test_user_can_update_own_file(self):
        stored_file = self.upload_file_as_user(
            self.user,
        )

        url = reverse(
            "file-detail",
            kwargs={"file_id": stored_file.id},
        )

        response = self.client.patch(
            url,
            {
                "original_name": "renamed.txt",
                "comment": "Изменённый комментарий",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        stored_file.refresh_from_db()

        self.assertEqual(
            stored_file.original_name,
            "renamed.txt",
        )

        self.assertEqual(
            stored_file.comment,
            "Изменённый комментарий",
        )

    def test_user_cannot_update_another_users_file(self):
        stored_file = self.upload_file_as_user(
            self.other_user,
        )

        self.client.force_authenticate(
            user=self.user,
        )

        url = reverse(
            "file-detail",
            kwargs={"file_id": stored_file.id},
        )

        response = self.client.patch(
            url,
            {
                "original_name": "hacked.txt",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_user_can_download_own_file(self):
        stored_file = self.upload_file_as_user(
            self.user,
        )

        url = reverse(
            "file-download",
            kwargs={"file_id": stored_file.id},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response["Content-Disposition"],
            'attachment; filename="test.txt"',
        )

        stored_file.refresh_from_db()

        self.assertIsNotNone(
            stored_file.last_downloaded_at,
        )

    def test_other_user_cannot_download_file(self):
        stored_file = self.upload_file_as_user(
            self.user,
        )

        self.client.force_authenticate(
            user=self.other_user,
        )

        url = reverse(
            "file-download",
            kwargs={"file_id": stored_file.id},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_admin_can_download_another_users_file(self):
        stored_file = self.upload_file_as_user(
            self.user,
        )

        self.client.force_authenticate(
            user=self.admin,
        )

        url = reverse(
            "file-download",
            kwargs={"file_id": stored_file.id},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_public_link_downloads_file_without_authentication(self):
        stored_file = self.upload_file_as_user(
            self.user,
        )

        self.client.force_authenticate(
            user=None,
        )

        url = reverse(
            "public-file-download",
            kwargs={"token": stored_file.public_token},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response["Content-Disposition"],
            'attachment; filename="test.txt"',
        )

    def test_user_can_delete_own_file(self):
        stored_file = self.upload_file_as_user(
            self.user,
        )

        file_name = stored_file.file.name
        self.assertTrue(
            stored_file.file.storage.exists(file_name),
        )

        url = reverse(
            "file-detail",
            kwargs={"file_id": stored_file.id},
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            StoredFile.objects.filter(
                id=stored_file.id,
            ).exists(),
        )

        self.assertFalse(
            stored_file.file.storage.exists(file_name),
        )

    def test_other_user_cannot_delete_file(self):
        stored_file = self.upload_file_as_user(
            self.user,
        )

        self.client.force_authenticate(
            user=self.other_user,
        )

        url = reverse(
            "file-detail",
            kwargs={"file_id": stored_file.id},
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
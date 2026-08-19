from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User

from .models import StoredFile


class StorageApiTests(APITestCase):
    def setUp(self):
        self.file_upload_url = reverse(
            "file-upload",
        )

        self.files_url = reverse(
            "file-list",
        )

        self.user = User.objects.create_user(
            username="testuser",
            full_name="Тестовый пользователь",
            email="test@example.com",
            password="TestPassword1!",
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            full_name="Другой пользователь",
            email="other@example.com",
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

    def create_uploaded_file(
        self,
        filename="test.txt",
        content=b"test file content",
        content_type="text/plain",
    ):
        return SimpleUploadedFile(
            filename,
            content,
            content_type=content_type,
        )

    def upload_file(
        self,
        user=None,
        filename="test.txt",
        content=b"test file content",
        content_type="text/plain",
        comment="",
    ):
        self.client.force_authenticate(
            user=user or self.user,
        )

        uploaded_file = self.create_uploaded_file(
            filename=filename,
            content=content,
            content_type=content_type,
        )

        return self.client.post(
            self.file_upload_url,
            {
                "file": uploaded_file,
                "comment": comment,
            },
            format="multipart",
        )

    def test_authenticated_user_can_upload_file(self):
        response = self.upload_file()

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            StoredFile.objects.count(),
            1,
        )

        stored_file = StoredFile.objects.get()

        self.assertEqual(
            stored_file.owner,
            self.user,
        )

        self.assertEqual(
            stored_file.original_name,
            "test.txt",
        )

        self.assertEqual(
            stored_file.size,
            len(b"test file content"),
        )

    def test_unauthenticated_user_cannot_upload_file(self):
        uploaded_file = self.create_uploaded_file()

        response = self.client.post(
            self.file_upload_url,
            {
                "file": uploaded_file,
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_authenticated_user_can_list_files(self):
        self.upload_file(
            filename="own-file.txt",
        )

        response = self.client.get(
            self.files_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["original_name"],
            "own-file.txt",
        )

    def test_user_does_not_see_other_user_files(self):
        self.upload_file(
            user=self.other_user,
            filename="other-file.txt",
        )

        self.client.force_authenticate(
            user=self.user,
        )

        response = self.client.get(
            self.files_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data,
            [],
        )

    def test_admin_can_list_all_files(self):
        self.upload_file(
            user=self.user,
            filename="user-file.txt",
        )

        self.upload_file(
            user=self.other_user,
            filename="other-file.txt",
        )

        self.client.force_authenticate(
            user=self.admin,
        )

        response = self.client.get(
            self.files_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        filenames = {
            item["original_name"]
            for item in response.data
        }

        self.assertIn(
            "user-file.txt",
            filenames,
        )

        self.assertIn(
            "other-file.txt",
            filenames,
        )

    def test_user_can_download_own_file(self):
        upload_response = self.upload_file()

        self.assertEqual(
            upload_response.status_code,
            status.HTTP_201_CREATED,
        )

        file_id = upload_response.data["id"]

        download_url = reverse(
            "file-download",
            kwargs={
                "file_id": file_id,
            },
        )

        response = self.client.get(
            download_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            'filename="test.txt"',
            response["Content-Disposition"],
        )

        content = b"".join(
            response.streaming_content,
        )

        self.assertEqual(
            content,
            b"test file content",
        )

    def test_admin_can_download_other_user_file(self):
        upload_response = self.upload_file(
            user=self.user,
        )

        file_id = upload_response.data["id"]

        download_url = reverse(
            "file-download",
            kwargs={
                "file_id": file_id,
            },
        )

        self.client.force_authenticate(
            user=self.admin,
        )

        response = self.client.get(
            download_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        content = b"".join(
            response.streaming_content,
        )

        self.assertEqual(
            content,
            b"test file content",
        )

    def test_other_user_cannot_download_other_users_file(self):
        upload_response = self.upload_file(
            user=self.user,
        )

        file_id = upload_response.data["id"]

        download_url = reverse(
            "file-download",
            kwargs={
                "file_id": file_id,
            },
        )

        self.client.force_authenticate(
            user=self.other_user,
        )

        response = self.client.get(
            download_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_public_file_can_be_downloaded_without_authentication(
        self,
    ):
        upload_response = self.upload_file()

        self.assertEqual(
            upload_response.status_code,
            status.HTTP_201_CREATED,
        )

        public_token = upload_response.data[
            "public_token"
        ]

        public_url = reverse(
            "public-file-download",
            kwargs={
                "token": public_token,
            },
        )

        self.client.logout()

        response = self.client.get(
            public_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        content = b"".join(
            response.streaming_content,
        )

        self.assertEqual(
            content,
            b"test file content",
        )

    def test_user_can_update_own_file(self):
        upload_response = self.upload_file(
            comment="Старый комментарий",
        )

        file_id = upload_response.data["id"]

        detail_url = reverse(
            "file-detail",
            kwargs={
                "file_id": file_id,
            },
        )

        response = self.client.patch(
            detail_url,
            {
                "original_name": "renamed.txt",
                "comment": "Новый комментарий",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        stored_file = StoredFile.objects.get(
            id=file_id,
        )

        self.assertEqual(
            stored_file.original_name,
            "renamed.txt",
        )

        self.assertEqual(
            stored_file.comment,
            "Новый комментарий",
        )

    def test_other_user_cannot_update_file(self):
        upload_response = self.upload_file(
            user=self.user,
        )

        file_id = upload_response.data["id"]

        detail_url = reverse(
            "file-detail",
            kwargs={
                "file_id": file_id,
            },
        )

        self.client.force_authenticate(
            user=self.other_user,
        )

        response = self.client.patch(
            detail_url,
            {
                "comment": "Чужой комментарий",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_user_can_delete_own_file(self):
        upload_response = self.upload_file()

        self.assertEqual(
            upload_response.status_code,
            status.HTTP_201_CREATED,
        )

        file_id = upload_response.data["id"]

        stored_file = StoredFile.objects.get(
            id=file_id,
        )

        file_name = stored_file.file.name

        self.assertTrue(
            stored_file.file.storage.exists(
                file_name,
            ),
        )

        detail_url = reverse(
            "file-detail",
            kwargs={
                "file_id": file_id,
            },
        )

        response = self.client.delete(
            detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            StoredFile.objects.filter(
                id=file_id,
            ).exists(),
        )

        self.assertFalse(
            stored_file.file.storage.exists(
                file_name,
            ),
        )

    def test_other_user_cannot_delete_file(self):
        upload_response = self.upload_file(
            user=self.user,
        )

        file_id = upload_response.data["id"]

        detail_url = reverse(
            "file-detail",
            kwargs={
                "file_id": file_id,
            },
        )

        self.client.force_authenticate(
            user=self.other_user,
        )

        response = self.client.delete(
            detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertTrue(
            StoredFile.objects.filter(
                id=file_id,
            ).exists(),
        )

    def test_upload_rejects_file_above_size_limit(self):
        oversized_file = SimpleUploadedFile(
            "large.bin",
            b"x" * (
                settings.MAX_UPLOAD_SIZE_BYTES
                + 1
            ),
            content_type="application/octet-stream",
        )

        self.client.force_authenticate(
            user=self.user,
        )

        response = self.client.post(
            self.file_upload_url,
            {
                "file": oversized_file,
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "слишком большой",
            response.data["detail"],
        )
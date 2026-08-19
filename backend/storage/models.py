import uuid
from pathlib import Path

from django.conf import settings
from django.db import models


def user_file_upload_path(instance, filename):
    extension = Path(filename).suffix.lower()

    generated_name = (
        f"{uuid.uuid4().hex}{extension}"
    )

    return (
        f"users/{instance.owner_id}/"
        f"{generated_name}"
    )


class StoredFile(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stored_files",
        verbose_name="владелец",
    )

    original_name = models.CharField(
        "исходное имя",
        max_length=255,
    )

    file = models.FileField(
        "файл",
        upload_to=user_file_upload_path,
    )

    size = models.PositiveBigIntegerField(
        "размер",
        default=0,
    )

    comment = models.TextField(
        "комментарий",
        blank=True,
        default="",
    )

    uploaded_at = models.DateTimeField(
        "дата загрузки",
        auto_now_add=True,
    )

    last_downloaded_at = models.DateTimeField(
        "дата последнего скачивания",
        null=True,
        blank=True,
    )

    public_token = models.UUIDField(
        "токен публичной ссылки",
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    class Meta:
        ordering = [
            "-uploaded_at",
        ]
        verbose_name = "файл"
        verbose_name_plural = "файлы"

    def __str__(self):
        return self.original_name
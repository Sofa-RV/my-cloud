from rest_framework import serializers

from .models import StoredFile


class StoredFileSerializer(
    serializers.ModelSerializer,
):
    download_url = serializers.SerializerMethodField()

    public_url = serializers.SerializerMethodField()

    class Meta:
        model = StoredFile
        fields = [
            "id",
            "original_name",
            "comment",
            "size",
            "uploaded_at",
            "last_downloaded_at",
            "public_token",
            "download_url",
            "public_url",
        ]
        read_only_fields = [
            "id",
            "original_name",
            "size",
            "uploaded_at",
            "last_downloaded_at",
            "public_token",
            "download_url",
            "public_url",
        ]

    def get_download_url(self, obj):
        request = self.context.get(
            "request",
        )

        if request is None:
            return None

        return request.build_absolute_uri(
            f"/api/files/{obj.id}/download/",
        )

    def get_public_url(self, obj):
        request = self.context.get(
            "request",
        )

        if request is None:
            return None

        return request.build_absolute_uri(
            f"/api/files/public/{obj.public_token}/",
        )
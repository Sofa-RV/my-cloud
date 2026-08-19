import logging

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import StoredFile
from .serializers import StoredFileSerializer


logger = logging.getLogger(__name__)


class FileListView(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        queryset = StoredFile.objects.select_related(
            "owner",
        )

        if request.user.is_app_admin:
            owner_id = request.query_params.get(
                "owner_id",
            )

            if owner_id:
                return queryset.filter(
                    owner_id=owner_id,
                )

            return queryset

        return queryset.filter(
            owner=request.user,
        )

    def get(self, request):
        files = self.get_queryset(request)

        serializer = StoredFileSerializer(
            files,
            many=True,
            context={
                "request": request,
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def post(self, request):
        uploaded_file = request.FILES.get(
            "file",
        )

        if uploaded_file is None:
            return Response(
                {
                    "detail": (
                        "Файл не был передан."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        stored_file = StoredFile.objects.create(
            owner=request.user,
            original_name=uploaded_file.name,
            file=uploaded_file,
            size=uploaded_file.size,
            comment=request.data.get(
                "comment",
                "",
            ),
        )

        logger.info(
            "Файл загружен owner=%s filename=%s size=%s",
            request.user.username,
            uploaded_file.name,
            uploaded_file.size,
        )

        serializer = StoredFileSerializer(
            stored_file,
            context={
                "request": request,
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class FileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, file_id):
        file_object = get_object_or_404(
            StoredFile,
            id=file_id,
        )

        if (
            file_object.owner_id != request.user.id
            and not request.user.is_app_admin
        ):
            return None

        return file_object

    def patch(self, request, file_id):
        file_object = self.get_object(
            request,
            file_id,
        )

        if file_object is None:
            return Response(
                {
                    "detail": "Доступ запрещён.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        original_name = request.data.get(
            "original_name",
        )

        if original_name is not None:
            cleaned_name = original_name.strip()

            if not cleaned_name:
                return Response(
                    {
                        "detail": (
                            "Имя файла не может быть пустым."
                        ),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            file_object.original_name = cleaned_name

        comment = request.data.get(
            "comment",
        )

        if comment is not None:
            file_object.comment = comment

        fields_to_update = []

        if original_name is not None:
            fields_to_update.append(
                "original_name",
            )

        if comment is not None:
            fields_to_update.append(
                "comment",
            )

        if fields_to_update:
            file_object.save(
                update_fields=fields_to_update,
            )

        serializer = StoredFileSerializer(
            file_object,
            context={
                "request": request,
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request, file_id):
        file_object = self.get_object(
            request,
            file_id,
        )

        if file_object is None:
            return Response(
                {
                    "detail": "Доступ запрещён.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        filename = file_object.original_name

        if file_object.file:
            file_object.file.delete(
                save=False,
            )

        file_object.delete()

        logger.info(
            "Файл удалён owner=%s filename=%s",
            request.user.username,
            filename,
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class FileDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_id):
        file_object = get_object_or_404(
            StoredFile,
            id=file_id,
        )

        if (
            file_object.owner_id != request.user.id
            and not request.user.is_app_admin
        ):
            return Response(
                {
                    "detail": "Доступ запрещён.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        file_object.last_downloaded_at = (
            timezone.now()
        )

        file_object.save(
            update_fields=[
                "last_downloaded_at",
            ],
        )

        logger.info(
            "Файл скачан owner=%s filename=%s",
            request.user.username,
            file_object.original_name,
        )

        response = FileResponse(
            file_object.file.open("rb"),
            as_attachment=True,
            filename=file_object.original_name,
        )

        return response


class PublicFileDownloadView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        file_object = get_object_or_404(
            StoredFile,
            public_token=token,
        )

        file_object.last_downloaded_at = (
            timezone.now()
        )

        file_object.save(
            update_fields=[
                "last_downloaded_at",
            ],
        )

        logger.info(
            "Публичный файл скачан filename=%s",
            file_object.original_name,
        )

        return FileResponse(
            file_object.file.open("rb"),
            as_attachment=True,
            filename=file_object.original_name,
        )
from django.urls import path

from .views import FileDetailView
from .views import FileDownloadView
from .views import FileListView
from .views import FileUploadView
from .views import PublicFileDownloadView


urlpatterns = [
    path(
        "",
        FileListView.as_view(),
        name="file-list",
    ),
    path(
        "upload/",
        FileUploadView.as_view(),
        name="file-upload",
    ),
    path(
        "public/<uuid:token>/",
        PublicFileDownloadView.as_view(),
        name="public-file-download",
    ),
    path(
        "<int:file_id>/download/",
        FileDownloadView.as_view(),
        name="file-download",
    ),
    path(
        "<int:file_id>/",
        FileDetailView.as_view(),
        name="file-detail",
    ),
]
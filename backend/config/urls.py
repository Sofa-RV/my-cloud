from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import re_path

from .views import frontend_asset
from .views import frontend_index


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "api/auth/",
        include("accounts.urls"),
    ),
    path(
        "api/files/",
        include("storage.urls"),
    ),
    re_path(
        r"^assets/(?P<asset_path>.+)$",
        frontend_asset,
        name="frontend-asset",
    ),
    re_path(
        r"^(?!admin/|api/|media/|assets/).*$",
        frontend_index,
        name="frontend-index",
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
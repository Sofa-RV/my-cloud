from mimetypes import guess_type
from pathlib import Path

from django.conf import settings
from django.http import FileResponse
from django.http import Http404
from django.http import HttpResponse


def frontend_root():
    root = Path(
        settings.FRONTEND_DIST_DIR,
    ).resolve()

    print(
        "FRONTEND ROOT:",
        root,
    )

    return root


def safe_frontend_path(relative_path):
    root = frontend_root()

    normalized_path = str(
        relative_path,
    ).replace(
        "\\",
        "/",
    ).lstrip(
        "/",
    )

    file_path = (
        root
        / Path(normalized_path)
    ).resolve()

    print(
        "PATH DEBUG:",
        repr(relative_path),
        "->",
        file_path,
        "exists=",
        file_path.is_file(),
    )

from mimetypes import guess_type
from pathlib import Path

from django.conf import settings
from django.http import FileResponse
from django.http import Http404
from django.http import HttpResponse


def frontend_root():
    return Path(
        settings.FRONTEND_DIST_DIR,
    ).resolve()


def safe_frontend_path(relative_path):
    root = frontend_root()

    normalized_path = str(
        relative_path,
    ).replace(
        "\\",
        "/",
    ).lstrip(
        "/",
    )

    file_path = (
        root
        / Path(normalized_path)
    ).resolve()

    if file_path == root:
        raise Http404(
            "Путь к frontend-ресурсу пуст.",
        )

    if root not in file_path.parents:
        raise Http404(
            "Недопустимый путь к frontend-ресурсу.",
        )

    return file_path


def frontend_index(request):
    index_path = safe_frontend_path(
        "index.html",
    )

    if not index_path.is_file():
        raise Http404(
            f"Frontend index не найден: {index_path}",
        )

    return HttpResponse(
        index_path.read_text(
            encoding="utf-8",
        ),
        content_type=(
            "text/html; charset=utf-8"
        ),
    )


def frontend_asset(request, asset_path):
    file_path = safe_frontend_path(
        Path("assets") / asset_path,
    )

    if not file_path.is_file():
        raise Http404(
            f"Frontend-ресурс не найден: {file_path}",
        )

    content_type, encoding = guess_type(
        str(file_path),
    )

    if content_type is None:
        content_type = (
            "application/octet-stream"
        )

    response = FileResponse(
        file_path.open("rb"),
        content_type=content_type,
    )

    if encoding:
        response["Content-Encoding"] = encoding

    return response
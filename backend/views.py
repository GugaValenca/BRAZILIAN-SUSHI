import mimetypes
from pathlib import Path

from django.contrib.staticfiles import finders
from django.http import FileResponse, Http404, JsonResponse


def serve_static_asset(_request, path: str):
    normalized = Path(path)
    if normalized.is_absolute() or ".." in normalized.parts:
        raise Http404("Static asset not found.")

    absolute_path = finders.find(path)
    if not absolute_path:
        raise Http404("Static asset not found.")

    content_type, _ = mimetypes.guess_type(absolute_path)
    return FileResponse(open(absolute_path, "rb"), content_type=content_type)


def health_check(_request):
    return JsonResponse({"status": "ok", "service": "brazilian-sushi-api"})

from http import HTTPStatus
from typing import Union

from django.conf import settings
from django.http import FileResponse, HttpRequest, HttpResponse


def download_image(
    request: HttpRequest, file_name: str
) -> Union[FileResponse, HttpResponse]:
    """скачиваем картинку"""
    file_name = str(settings.BASE_DIR) + file_name
    try:
        return FileResponse(open(file_name, 'rb'), as_attachment=True)
    except Exception:
        return HttpResponse(status=HTTPStatus.NOT_FOUND)

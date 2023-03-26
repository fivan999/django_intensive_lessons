from typing import Union

from django.conf import settings
from django.http import FileResponse, Http404, HttpRequest, HttpResponse
from django.views import View


class DownloadImageView(View):
    """скачиваем картинку"""
    def get(
            self,
            request: HttpRequest,
            file_name: str
    ) -> Union[FileResponse, HttpResponse]:
        """По запросу get возвращаем файл или ошибку 404"""
        file_name = str(settings.BASE_DIR) + file_name
        try:
            return FileResponse(open(file_name, 'rb'), as_attachment=True)
        except Exception:
            return Http404

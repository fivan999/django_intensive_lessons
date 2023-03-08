from django.apps import AppConfig


class DownloadConfig(AppConfig):
    """базовый класс для приложения Download"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'download'
    verbose_name = 'скачивание'

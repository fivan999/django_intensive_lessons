from django.apps import AppConfig


class HomepageConfig(AppConfig):
    """Базовый класс для приложения homepage"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'homepage'
    verbose_name = 'домашняя страница'

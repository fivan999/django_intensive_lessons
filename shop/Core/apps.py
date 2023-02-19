from django.apps import AppConfig


class CoreConfig(AppConfig):
    """базовый класс для приложения Core"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Core'

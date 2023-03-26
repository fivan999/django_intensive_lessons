from django.apps import AppConfig


class RatingConfig(AppConfig):
    """базовый класс для приложения Rating"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rating'
    verbose_name = 'рейтинг'

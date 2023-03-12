from django.apps import AppConfig


class FeedbackConfig(AppConfig):
    """базовый класс для приложения feedback"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feedback'
    verbose_name = 'обратная связь'

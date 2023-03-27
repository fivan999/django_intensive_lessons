from django.apps import AppConfig


class StatisticConfig(AppConfig):
    """базовый класс приложения statistic"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'statistic'
    verbose_name = 'статистика'

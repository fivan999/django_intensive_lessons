from django.apps import AppConfig


class BasketConfig(AppConfig):
    """базовый класс для приложения basket"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'basket'
    verbose_name = 'корзина'

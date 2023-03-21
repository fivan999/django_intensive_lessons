from django.apps import AppConfig


class UsersConfig(AppConfig):
    """базовый класс для приложения Users"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'пользователи'

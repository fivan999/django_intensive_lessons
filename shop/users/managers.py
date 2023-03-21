import django.db.models
from django.contrib.auth.models import UserManager


class ShopUserManager(UserManager):
    """менеджер модели ShopUser"""

    def get_active_users_list(self) -> django.db.models.QuerySet:
        """возвращаем активных пользователей"""
        return self.get_queryset().filter(
            is_active=True
        ).select_related('profile')

    def get_only_useful_list_fields(self) -> django.db.models.QuerySet:
        """только нужные поля для списка пользователей"""
        return self.get_active_users_list().only(
            'username', 'email', 'profile__image'
        )

    def get_only_useful_detail_fields(self) -> django.db.models.QuerySet:
        """только нужные поля для одного пользователя"""
        return self.get_active_users_list().only(
            'username', 'email', 'profile__image', 'first_name', 'last_name',
            'profile__coffee_count', 'profile__birthday'
        )

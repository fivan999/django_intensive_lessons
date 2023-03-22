import django.db.models
from django.contrib.auth.models import UserManager

import users.models


class ShopUserManager(UserManager):
    """менеджер модели ShopUser"""

    def get_queryset(self) -> django.db.models.QuerySet:
        """возвращаем активных пользователей"""
        return super().get_queryset().filter(
            is_active=True
        ).select_related('profile')

    def get_only_useful_list_fields(self) -> django.db.models.QuerySet:
        """только нужные поля для списка пользователей"""
        return self.get_queryset().only(
            'username', 'email', 'profile__image'
        )

    def get_only_useful_detail_fields(self) -> django.db.models.QuerySet:
        """только нужные поля для одного пользователя"""
        return self.get_queryset().only(
            'username', 'email', 'profile__image', 'first_name', 'last_name',
            'profile__coffee_count', 'profile__birthday'
        )

    def create_superuser(self, username, email, password, **extra_fields):
        """переопределяем создание суперпользователя"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        user.save(using=self._db)
        users.models.Profile.objects.create(user=user)
        return user

import django.db.models
from django.contrib.auth.models import UserManager
from django.core.exceptions import ValidationError

import users.models


class ShopUserManager(UserManager):
    """менеджер модели ShopUser"""

    def get_active_users_list(self) -> django.db.models.QuerySet:
        """возвращаем активных пользователей"""
        return (
            self.get_queryset()
            .filter(is_active=True)
            .select_related('profile')
        )

    def get_only_useful_list_fields(self) -> django.db.models.QuerySet:
        """только нужные поля для списка пользователей"""
        return self.get_active_users_list().only(
            'username', 'email', 'profile__image'
        )

    def get_only_useful_detail_fields(self) -> django.db.models.QuerySet:
        """только нужные поля для одного пользователя"""
        return self.get_active_users_list().only(
            'username',
            'email',
            'profile__image',
            'first_name',
            'last_name',
            'profile__coffee_count',
            'profile__birthday',
        )

    @classmethod
    def normalize_email(cls, email):
        """добавляем катомную нормализацию email"""
        if not email:
            return ''
        email_user, email_domain = email.lower().strip().split('@')

        if '+' in email_user:
            email_user = email_user[: email_user.find('+')]

        if email_domain in ('yandex.ru', 'ya.ru'):
            email_user = email_user.replace('.', '-')
            email_domain = 'yandex.ru'
        elif email_domain == 'gmail.com':
            email_user = email_user.replace('.', '')

        return f'{email_user}@{email_domain}'

    def create_superuser(self, username, email, password, **extra_fields):
        """переопределяем создание суперпользователя"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        email = self.normalize_email(email)
        if users.models.ShopUser.objects.filter(email=email).exists():
            raise ValidationError('Пользователь уже существует')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        user.save(using=self._db)
        users.models.Profile.objects.create(user=user)
        return user

import core.models

import django.db.models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from transliterate import translit

import users.managers


def generate_image_path(obj: django.db.models.Model, filename: str) -> str:
    """генерируем файловый пусть к картинке"""
    filename = translit(filename, 'ru', reversed=True)
    return f'users/{obj.user.pk}/{filename}'


class ShopUser(AbstractUser):
    """наш кастомный пользователь"""

    objects = users.managers.ShopUserManager()

    email = django.db.models.EmailField(
        _('email address'), blank=True, unique=True
    )

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'
        swappable = 'AUTH_USER_MODEL'

    def get_absolute_url(self) -> str:
        """путь к user_detail"""
        return reverse('users:user_detail', kwargs={'user_id': self.pk})


class Profile(core.models.AbstractImageModel):
    """модель профиля пользователя"""

    user = django.db.models.OneToOneField(
        ShopUser,
        related_name='profile',
        verbose_name='профиль',
        help_text='Профиль пользователя',
        on_delete=django.db.models.CASCADE,
        blank=True,
        null=True
    )
    birthday = django.db.models.DateField(
        blank=True,
        verbose_name='дата рождения',
        help_text='Дата рождения пользователя',
        null=True
    )
    image = django.db.models.ImageField(
        blank=True,
        verbose_name='аватарка',
        help_text='Аватарка пользователя',
        upload_to=generate_image_path,
        null=True
    )
    coffee_count = django.db.models.IntegerField(
        default=0,
        verbose_name='количесто кофе',
        help_text='Сколько раз пользователь пытался сварить кофе'
    )

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'
        db_table = 'users_profile'

    def __str__(self) -> str:
        """строковое представление профиля"""
        return f'Профиль пользователя {self.user.pk}'

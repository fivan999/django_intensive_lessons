from catalog.models import Item

import django.db.models

from users.models import ShopUser


class Basket(django.db.models.Model):
    """модель корзины"""
    item = django.db.models.ForeignKey(
        Item,
        verbose_name='товар',
        help_text='Товар из корзины пользователя',
        on_delete=django.db.models.CASCADE,
        related_name='basket_items'
    )
    user = django.db.models.ForeignKey(
        ShopUser,
        verbose_name='пользователь',
        help_text='Пользователь, добавивщий товар в корзину',
        on_delete=django.db.models.CASCADE,
        related_name='basket_items'
    )

    class Meta:
        db_table = 'basket_basket'
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

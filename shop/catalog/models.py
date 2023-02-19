import Core.models

import catalog.validators

import django.core.validators
import django.db.models


class Tag(Core.models.AbstractCatalogModelWithSlug):
    """модель Tag"""

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        db_table = 'catalog_tag'


class Category(Core.models.AbstractCatalogModelWithSlug):
    """модель Category"""

    weight = django.db.models.PositiveSmallIntegerField(
        'Вес',
        help_text=(
            'Введите вес товара (положительное целое число от 0 до 32767)'
        ),
        default=100
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'catalog_category'


class Item(Core.models.AbstractCatalogModel):
    """модель Item"""

    text = django.db.models.TextField(
        'Описание',
        help_text='Введите описание',
        validators=[
            catalog.validators.awesome_validator,
        ]
    )
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        related_name='catalog_items',
        help_text='Категория, к которой принадлежит товар'
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        related_name='catalog_items',
        help_text='Тэги товара'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        db_table = 'catalog_item'

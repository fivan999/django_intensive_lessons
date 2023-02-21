import catalog.validators

import core.models

import django.core.validators
import django.db.models


class Tag(core.models.AbstractCatalogModelWithSlug):
    """модель Tag"""

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        db_table = 'catalog_tag'


class Category(core.models.AbstractCatalogModelWithSlug):
    """модель Category"""

    weight = django.db.models.PositiveSmallIntegerField(
        verbose_name='Вес',
        help_text=(
            'Введите вес товара (положительное целое число от 0 до 32767)'
        ),
        validators=[
            django.core.validators.MaxValueValidator(32767),
            django.core.validators.MinValueValidator(0),
        ],
        default=100
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'catalog_category'


class Item(core.models.AbstractCatalogModel):
    """модель Item"""

    text = django.db.models.TextField(
        verbose_name='Описание',
        help_text='Введите описание',
        validators=[
            catalog.validators.awesome_validator,
        ]
    )
    category = django.db.models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=django.db.models.CASCADE,
        related_name='catalog_items',
        help_text='Категория, к которой принадлежит товар'
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        related_name='catalog_items',
        help_text='Тэги товара'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        db_table = 'catalog_item'

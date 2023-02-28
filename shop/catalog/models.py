import catalog.validators

from ckeditor.fields import RichTextField

import core.models

import django.core.validators
import django.db.models
from django.urls import reverse


class Tag(
    core.models.AbstractNameTextModel,
    core.models.AbstractSlugModel,
    core.models.AbstractKeywordModel
):
    """модель Tag"""

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'
        db_table = 'catalog_tag'


class Category(
    core.models.AbstractNameTextModel,
    core.models.AbstractSlugModel,
    core.models.AbstractKeywordModel
):
    """модель Category"""

    weight = django.db.models.PositiveSmallIntegerField(
        verbose_name='вес',
        help_text=(
            'Введите вес товара (положительное целое число от 1 до 32767)'
        ),
        validators=[
            django.core.validators.MaxValueValidator(32767),
            django.core.validators.MinValueValidator(1),
        ],
        default=100
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        db_table = 'catalog_category'


class Item(core.models.AbstractNameTextModel):
    """модель Item"""

    text = RichTextField(
        verbose_name='описание',
        help_text='Введите описание',
        validators=[
            catalog.validators.ValidateMustContain('превосходно', 'роскошно'),
        ]
    )
    category = django.db.models.ForeignKey(
        Category,
        verbose_name='категория',
        on_delete=django.db.models.CASCADE,
        related_name='catalog_items',
        help_text='Категория, к которой принадлежит товар'
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        verbose_name='тэги',
        related_name='catalog_items',
        help_text='Тэги товара'
    )

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        db_table = 'catalog_item'

    def get_absolute_url(self) -> str:
        """путь к item_detail"""
        return reverse('item_detail', kwargs={'item_num': self.pk})


class ImageToItem(core.models.AbstractImageModel):
    """модель Image"""

    item = django.db.models.OneToOneField(
        Item,
        verbose_name='превью',
        related_name='main_image',
        on_delete=django.db.models.CASCADE,
        help_text='Главное изображение для товара'
    )

    class Meta:
        verbose_name = 'главное изображение'
        verbose_name_plural = 'главные изображения'
        db_table = 'catalog_image'


class GaleryToItem(core.models.AbstractImageModel):
    """модель Galery"""

    item = django.db.models.ForeignKey(
        Item,
        verbose_name='галерея',
        related_name='galery',
        on_delete=django.db.models.CASCADE
    )

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'галерея изображений'
        db_table = 'catalog_galery'

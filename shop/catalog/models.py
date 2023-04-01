import catalog.managers
import catalog.validators

from ckeditor.fields import RichTextField

import core.models

import django.core.validators
import django.db.models
from django.conf import settings
from django.urls import reverse
from django.utils.html import mark_safe


class Tag(
    core.models.AbstractNameTextModel,
    core.models.AbstractSlugModel,
    core.models.AbstractKeywordModel,
):
    """модель Tag"""

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'
        db_table = 'catalog_tag'


class Category(
    core.models.AbstractNameTextModel,
    core.models.AbstractSlugModel,
    core.models.AbstractKeywordModel,
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
        default=100,
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        db_table = 'catalog_category'


class Item(core.models.AbstractNameTextModel):
    """модель Item"""

    objects = catalog.managers.ItemManager()

    text = RichTextField(
        verbose_name='описание',
        help_text='Введите описание',
        validators=[
            catalog.validators.ValidateMustContain(
                *settings.NESSESARY_TEXT_WORDS
            ),
        ],
    )
    category = django.db.models.ForeignKey(
        Category,
        verbose_name='категория',
        on_delete=django.db.models.CASCADE,
        related_name='catalog_items',
        help_text='Категория, к которой принадлежит товар',
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        verbose_name='тэги',
        related_name='catalog_items',
        help_text='Тэги товара',
    )
    is_on_main = django.db.models.BooleanField(
        verbose_name='на главной',
        help_text='Отображать ли товар на главной странице',
        default=False,
    )
    created_at = django.db.models.DateField(
        auto_now_add=True,
        verbose_name='дата создания',
        help_text='Дата создания товара',
    )
    updated_at = django.db.models.DateField(
        auto_now=True,
        verbose_name='дата изменения',
        help_text='Дата изменения товара',
    )
    price = django.db.models.PositiveIntegerField(
        verbose_name='цена',
        help_text='Цена товара',
        default=1000
    )

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        db_table = 'catalog_item'

    def image_thumb(self):
        """вывод изображения"""
        if self.main_image:
            return mark_safe(
                f'<img src="{self.main_image.get_image_50x50().url}">'
            )
        return 'Нет изображения'

    image_thumb.short_description = 'картинка'

    def get_absolute_url(self) -> str:
        """путь к item_detail"""
        return reverse('catalog:item_detail', kwargs={'pk': self.pk})


class ImageToItem(core.models.AbstractImageModel):
    """модель Image"""

    item = django.db.models.OneToOneField(
        Item,
        verbose_name='превью',
        related_name='main_image',
        on_delete=django.db.models.CASCADE,
        help_text='Главное изображение для товара',
    )

    class Meta:
        verbose_name = 'главное изображение'
        verbose_name_plural = 'главные изображения'
        db_table = 'catalog_image'

    def __str__(self) -> str:
        """строковое представление главной картинки"""
        return f'Главная картинка {self.pk}'


class GaleryToItem(core.models.AbstractImageModel):
    """модель Galery"""

    item = django.db.models.ForeignKey(
        Item,
        verbose_name='галерея',
        related_name='galery',
        on_delete=django.db.models.CASCADE,
    )

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'галерея изображений'
        db_table = 'catalog_galery'

    def __str__(self) -> str:
        """строковое представление картинки из галереи"""
        return f'Картинка из гелереи {self.pk}'

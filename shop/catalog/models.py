import catalog.validators

import core.models
from core.utils import normalize_models_name

import django.core.validators
import django.db.models
from django.core.exceptions import ValidationError


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

    def clean(self, *args, **kwargs) -> None:
        normalized_name = normalize_models_name(self.name)
        for item in Tag.objects.all():
            if item.keyword == normalized_name:
                raise ValidationError('Уже есть категория с похожим именем')
        self.keyword = normalized_name
        super(Tag, self).clean(*args, **kwargs)


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

    def clean(self, *args, **kwargs) -> None:
        normalized_name = normalize_models_name(self.name)
        for item in Category.objects.all():
            if item.keyword == normalized_name:
                raise ValidationError('Уже есть тэг с похожим именем')
        self.keyword = normalized_name
        super(Category, self).clean(*args, **kwargs)


class Item(core.models.AbstractNameTextModel):
    """модель Item"""

    text = django.db.models.TextField(
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

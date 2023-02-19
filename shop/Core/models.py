import catalog.validators

import django.db.models


class AbstractCatalogModel(django.db.models.Model):
    """абстрактая модель для Catalog"""

    is_published = django.db.models.BooleanField(
        'Опубликован',
        help_text='Опубликован или нет',
        default=True
    )
    name = django.db.models.CharField(
        'Имя',
        help_text='Введите имя',
        max_length=150
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:15]


class AbstractCatalogModelWithSlug(AbstractCatalogModel):
    """абстрактная модель для Catalog с полем slug"""

    slug = django.db.models.CharField(
        'Уникальное поле',
        help_text='Уникальное для каждого элемента поле',
        validators=[
            catalog.validators.slug_validator,
        ],
        unique=True,
        max_length=200
    )

    class Meta:
        abstract = True

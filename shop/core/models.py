import django.core.validators
import django.db.models


class AbstractCatalogModel(django.db.models.Model):
    """абстрактая модель для Catalog"""

    is_published = django.db.models.BooleanField(
        verbose_name='Опубликован',
        help_text='Опубликован или нет',
        default=True
    )
    name = django.db.models.CharField(
        verbose_name='Имя',
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
        verbose_name='Уникальное поле',
        help_text='Уникальное для каждого элемента поле',
        validators=[
            django.core.validators.validate_slug,
        ],
        unique=True,
        max_length=200
    )

    class Meta:
        abstract = True

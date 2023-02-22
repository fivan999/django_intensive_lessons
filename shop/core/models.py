import django.core.validators
import django.db.models


class AbstractNameTextModel(django.db.models.Model):
    """абстрактая модель для Catalog"""

    is_published = django.db.models.BooleanField(
        verbose_name='опубликован',
        help_text='Опубликован или нет',
        default=True
    )
    name = django.db.models.CharField(
        verbose_name='имя',
        help_text='Введите имя',
        max_length=150
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name[:15]


class AbstractSlugModel(django.db.models.Model):
    """абстрактная модель для Catalog с полем slug"""

    slug = django.db.models.SlugField(
        verbose_name='уникальное поле',
        help_text='Уникальное для каждого элемента поле',
        validators=[
            django.core.validators.validate_slug,
        ],
        unique=True,
        max_length=200
    )

    class Meta:
        abstract = True

import re
import secrets

import django.core.validators
import django.db.models
from django.core.exceptions import ValidationError

from sorl.thumbnail import get_thumbnail
from transliterate import translit


def generate_image_path(obj: django.db.models.Model, filename: str) -> str:
    """генерируем файловый пусть к картинке"""
    filename = translit(filename, 'ru', reverse=True)
    filename = (
        filename[: filename.rfind('.')]
        + secrets.token_hex(6)
        + filename[filename.rfind('.') :]
    )
    return f'catalog/{obj.item.pk}/{filename}'


class AbstractNameTextModel(django.db.models.Model):
    """абстрактая модель для Catalog"""

    is_published = django.db.models.BooleanField(
        verbose_name='опубликован',
        help_text='Опубликован или нет',
        default=True,
    )
    name = django.db.models.CharField(
        verbose_name='имя', help_text='Введите имя', max_length=150
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
        unique=True,
        max_length=200,
    )

    class Meta:
        abstract = True


class AbstractKeywordModel(django.db.models.Model):
    """абстрактная модель с полем keyword"""

    keyword = django.db.models.CharField(editable=False, max_length=150)

    class Meta:
        abstract = True

    def clean(self, *args, **kwargs) -> None:
        """переопределение метода clean"""
        normalized_name = self.normalize_models_name(self.name)
        if (
            self.__class__.objects.filter(keyword=normalized_name)
            .exclude(id=self.id)
            .count()
            > 0
        ):
            raise ValidationError('Уже есть тэг с похожим именем')
        self.keyword = normalized_name
        super().clean(*args, **kwargs)

    @staticmethod
    def normalize_models_name(value: str) -> str:
        """нормализуем имя модели"""
        # похожие русские буквы заменяем на английские
        replace_letters = {
            'е': 'e',
            'о': 'o',
            'с': 'c',
            'х': 'x',
            'а': 'a',
            'у': 'y',
            'р': 'p',
            'м': 'm',
            'т': 't',
        }
        result = ''
        for symbol in value.lower():
            if re.fullmatch('[а-яa-z0-9]', symbol):
                result += replace_letters.get(symbol, symbol)
        return result


class AbstractImageModel(django.db.models.Model):
    """абстрактная модель с картинкой"""

    image = django.db.models.ImageField(
        verbose_name='картинка',
        upload_to=generate_image_path,
        help_text='Загрузите картинку',
    )

    def get_image_300x300(self):
        """обрезаем картинку(для каталога)"""
        return get_thumbnail(self.image, '300x300', crop='center', quality=65)

    def get_image_50x50(self):
        """обрезаем картинку(для админки)"""
        return get_thumbnail(self.image, '50x50', crop='center', quality=60)

    class Meta:
        abstract = True

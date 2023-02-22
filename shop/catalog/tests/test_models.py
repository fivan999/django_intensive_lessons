from catalog.models import (
    Category,
    Item,
    Tag
)

from django.core.exceptions import ValidationError
from django.test import TestCase

from parameterized import parameterized


class ModelsTests(TestCase):
    """тестируем модели"""

    @classmethod
    def setUpClass(cls) -> None:
        """настройки перед тестированием"""
        super().setUpClass()

        cls.category = Category.objects.create(
            is_published=True,
            name='Тестовая категория',
            slug='test_slug',
            weight=100
        )

        cls.tag = Tag.objects.create(
            is_published=True,
            name='Тестовый тэг',
            slug='test_slug'
        )

    @parameterized.expand(
        [
            '', 'a' * 151,
        ]
    )
    def test_create_invalid_name(self, test_case: str) -> None:
        """тестируем создание невалидного name"""
        start_count = Item.objects.count()

        with self.assertRaises(ValidationError):
            self.item = Item(
                name=test_case,
                text='превосходно',
                category=self.category
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(self.tag)

        self.assertEqual(
            Item.objects.count(),
            start_count,
            f'Ошибка создания name модели: {test_case}'
        )

    @parameterized.expand(
        [
            '$' * 149, 'b' * 150, 'aboba', 'олежа',
        ]
    )
    def test_create_valid_name(self, test_case: str) -> None:
        """тестируем создание валидного name"""
        start_count = Item.objects.count()

        self.item = Item(
            name=test_case,
            text='превосходно',
            category=self.category
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(self.tag)

        self.assertEqual(
            Item.objects.count(),
            start_count + 1,
            f'Ошибка создания name модели: {test_case}'
        )

    @parameterized.expand(
        [
            'круто',
            'aboba',
            'oleg',
            '',
            'П!ревосходно',
            'Ро!7кошно',
            'Нероскошно',
            '1превосходно',
        ]
    )
    def test_create_invalid_text(self, test_case: str) -> None:
        """тестируем создание невалидного text"""
        start_count = Item.objects.count()

        with self.assertRaises(ValidationError):
            self.item = Item(
                name='aboba',
                text=test_case,
                category=self.category
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(self.tag)

        self.assertEqual(
            Item.objects.count(),
            start_count,
            f'Ошибка создания text модели: {test_case}'
        )

    @parameterized.expand(
        [
            ',роскошно ',
            'превосходно',
            ', Превосходно: фищиф',
            'nigbob like Роскошно',
            'bebra_dev Превосходно воркает',
        ]
    )
    def test_create_valid_text(self, test_case: str) -> None:
        """тестируем создание валидного text"""
        start_count = Item.objects.count()

        self.item = Item(
            name='aboba',
            text=test_case,
            category=self.category
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(self.tag)

        self.assertEqual(
            Item.objects.count(),
            start_count + 1,
            f'Ошибка создания text модели: {test_case}'
        )

    @parameterized.expand(
        [
            ' роскошно ', '#1aboba-_', '12-_иван', '', '1' * 201,
        ]
    )
    def test_create_invalid_slug(self, test_case: str) -> None:
        """тестируем создание невалидного slug"""
        start_count = Tag.objects.count()

        with self.assertRaises(ValidationError):
            self.item = Tag(
                name='олег',
                slug=test_case
            )
            self.item.full_clean()
            self.item.save()

        self.assertEqual(
            Tag.objects.count(),
            start_count,
            f'Ошибка создания slug модели: {test_case}'
        )

    @parameterized.expand(
        [
            '1aboba_-', '1234567', '----', '____', '_-',
        ]
    )
    def test_create_valid_slug(self, test_case: str) -> None:
        """тестируем создание валидного slug"""
        start_count = Tag.objects.count()

        self.item = Tag(
            name='олег',
            slug=test_case
        )
        self.item.full_clean()
        self.item.save()

        self.assertEqual(
            Tag.objects.count(),
            start_count + 1,
            f'Ошибка создания slug модели: {test_case}'
        )

    @parameterized.expand([(-1,), (-32767,), (32768,), (0,)])
    def test_create_invalid_weight(self, test_case: int) -> None:
        """тестируем создание невалидного weight"""
        start_count = Category.objects.count()

        with self.assertRaises(ValidationError):
            self.item = Category(
                name='олег',
                slug='aboba',
                weight=test_case
            )
            self.item.full_clean()
            self.item.save()

        self.assertEqual(
            Category.objects.count(),
            start_count,
            f'Ошибка создания weight модели: {test_case}'
        )

    @parameterized.expand([(1,), (32767,), (15000,)])
    def test_create_valid_weight(self, test_case: int) -> None:
        """тестируем создание валидного weight"""
        start_count = Category.objects.count()

        self.item = Category(
            name='олег',
            slug='aboba',
            weight=test_case
        )
        self.item.full_clean()
        self.item.save()

        self.assertEqual(
            Category.objects.count(),
            start_count + 1,
            f'Ошибка создания weight модели: {test_case}'
        )

    def tearDown(self):
        """чистим бд после каждого теста"""
        Item.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        super(ModelsTests, self).tearDown()

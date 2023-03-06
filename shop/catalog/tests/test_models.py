from catalog.models import (
    Category,
    Item,
    Tag
)

import django.urls
from django.core.exceptions import ValidationError
from django.test import Client, TestCase

from parameterized import parameterized


class ModelsTests(TestCase):
    """тестируем модели"""

    def setUp(self) -> None:
        """настройки перед тестированием"""
        self.category = Category.objects.create(
            is_published=True,
            name='Тестовая категория',
            slug='test_slug',
            weight=100
        )

        self.tag = Tag.objects.create(
            is_published=True,
            name='Тестовый тэг',
            slug='test_slug'
        )
        super().setUp()

    def tearDown(self):
        """чистим бд после каждого теста"""
        Item.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        super().tearDown()

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


class ContextTests(TestCase):
    """тестируем модельки на страницах"""

    def setUp(self) -> None:
        """настройки перед тестами"""
        self.published_category = Category.objects.create(
            is_published=True,
            name='Тестовая опубликованная категория',
            slug='test_slug1',
            weight=100
        )
        self.unpublished_category = Category.objects.create(
            is_published=False,
            name='Тестовая неопубликованная категория',
            slug='test_slug2',
            weight=100
        )
        self.published_tag = Tag.objects.create(
            is_published=True,
            name='Тестовый опубликованный тэг',
            slug='test_slug1'
        )
        self.unpublished_tag = Tag.objects.create(
            is_published=False,
            name='Тестовый неопубликованный тэг',
            slug='test_slug2'
        )
        self.published_item = Item.objects.create(
            name='опубликованный товар',
            text='превосходно',
            is_published=True,
            category=self.published_category,
        )
        self.unpublished_item = Item.objects.create(
            name='неопубликованный товар',
            text='превосходно',
            is_published=False,
            category=self.published_category
        )
        self.published_item_on_main = Item.objects.create(
            name='опубликованный товар',
            text='превосходно',
            is_published=True,
            is_on_main=True,
            category=self.published_category,
        )

        self.unpublished_category.save()
        self.published_category.save()
        self.unpublished_tag.save()
        self.published_tag.save()

        self.published_item.clean()
        self.unpublished_item.clean()
        self.published_item_on_main.clean()

        self.published_item.save()
        self.unpublished_item.save()
        self.published_item_on_main.save()

        self.published_item.tags.add(self.published_tag)
        self.unpublished_item.tags.add(self.unpublished_tag)
        return super().setUp()

    def test_catalog_show_correct_context(self) -> None:
        """проверка корректного контекста в каталоге"""
        response = Client().get(django.urls.reverse('catalog:item_list'))
        self.assertIn('items', response.context)

    def test_catalog_correct_item_count(self) -> None:
        """проверка количества item в каталоге"""
        response = Client().get(django.urls.reverse('catalog:item_list'))
        items = response.context['items']
        self.assertEqual(items.count(), 2)

    def test_homepage_show_correct_context(self) -> None:
        """проверка корректного контекста на главной странице"""
        response = Client().get(django.urls.reverse('homepage:homepage'))
        self.assertIn('items', response.context)

    def test_homepage_correct_item_count(self) -> None:
        """проверка количества item на главной странице"""
        response = Client().get(django.urls.reverse('homepage:homepage'))
        items = response.context['items']
        self.assertEqual(items.count(), 1)

    @parameterized.expand(
        [
            [1, 200],
            [2, 404],
            [3, 200],
            [10, 404],
        ]
    )
    def test_item_detail_status_code(
        self, item_id: int, expected: bool
    ) -> None:
        """проверка статус кода в item_detail"""
        response = Client().get(
            django.urls.reverse('catalog:item_detail', args=[item_id])
        )
        self.assertEqual(response.status_code, expected)

    @parameterized.expand([(1,), (3,)])
    def test_item_detail_correct_context(self, item_id: int) -> None:
        """проверка корректного контекста в item_detail"""
        response = Client().get(
            django.urls.reverse('catalog:item_detail', args=[item_id])
        )
        self.assertIn('item', response.context)

    def tearDown(self) -> None:
        """чистим бд после каждого теста"""
        Item.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        super().tearDown()

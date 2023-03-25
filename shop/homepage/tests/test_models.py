import django.urls
from django.test import Client, TestCase

from catalog.models import Item


class ContextTests(TestCase):
    """тестируем модельки на страницах"""

    fixtures = [
        'fixtures/tests/context_tests.json',
    ]

    def test_homepage_show_correct_context(self) -> None:
        """проверка корректного контекста на главной странице"""
        response = Client().get(django.urls.reverse('homepage:homepage'))
        self.assertIn('items', response.context)

    def test_homepage_correct_context_model(self) -> None:
        """тестируем возвращает ли сервер Item на главной странице"""
        response = Client().get(django.urls.reverse('homepage:homepage'))
        self.assertEqual(
            isinstance(response.context['items'].first(), Item), True
        )

    def test_homepage_correct_item_count(self) -> None:
        """проверка количества item на главной странице"""
        response = Client().get(django.urls.reverse('homepage:homepage'))
        items = response.context['items']
        self.assertEqual(items.count(), 1)
